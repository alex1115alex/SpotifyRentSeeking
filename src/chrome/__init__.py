from webdriver_manager.chrome import ChromeDriverManager as CM
import random, string, re, io, tempfile, os, shutil

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from .patcher import Patcher

class Chrome():
    CHROMEDRIVER = None
    user_dir = None
    chrome_options = Options()

    def __init__(self):
        if not os.path.exists("data/driver"):
            os.makedirs("data/driver")
        chromedriver = CM(path=f"data/driver/chromedriver{random.randint(1000, 9999)}").install()
        Patcher.patch_exe = self.patch_binary(chromedriver)
        # self.CHROMEDRIVER = Service(chromedriver)
        self.CHROMEDRIVER = chromedriver
    
    def remove_chromedriver(self):
        shutil.rmtree(self.CHROMEDRIVER)

    def close_driver(self, driver):
        driver.close()
        shutil.rmtree(self.user_dir)
        shutil.rmtree("data/driver")

    def options(self, i=None, proxy=None, headless=False):
        # user_data_dir = os.path.normpath(tempfile.mkdtemp())
        # self.user_dir = user_data_dir
        # self.chrome_options.add_argument("--user-data-dir=%s" % user_data_dir)
        self.chrome_options.add_argument('--mute-audio')
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.chrome_options.add_argument('Content-Type="text/html"')
        if headless:
            self.chrome_options.add_argument("headless")
        # if proxy != None:
        #     self.chrome_options.add_argument("--proxy-server=" + proxy)
        self.chrome_options.add_argument('chartset=utf-8')
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-crash-reporter")
        self.chrome_options.add_argument("--disable-in-process-stack-traces")
        self.chrome_options.add_argument("--disable-logging")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--log-level=3")
        self.chrome_options.add_argument("--output=/dev/null")
        if proxy!=None and i!=None:
            if not os.path.exists("data/extension"):
                os.makedirs("data/extension")
            self.chrome_options.add_extension(f"data/extension/proxy_auth_plugin_{i}.zip")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en_US,en'})
        self.chrome_options.add_argument('--disable-features=UserAgentClientHint')
        webdriver.DesiredCapabilities.CHROME['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
        webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True
        return self.chrome_options

    def execute(self, driver):
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                            Object.defineProperty(window, 'navigator', {
                                value: new Proxy(navigator, {
                                has: (target, key) => (key === 'webdriver' ? false : key in target),
                                get: (target, key) =>
                                    key === 'webdriver'
                                    ? undefined
                                    : typeof target[key] === 'function'
                                    ? target[key].bind(target)
                                    : target[key]
                                })
                            });
                            
                                                    
                """
            },
        )
        driver.execute_cdp_cmd(
            "Network.setUserAgentOverride",
            {
                "userAgent": driver.execute_script(
                    "return navigator.userAgent"
                ).replace("Headless", "")
            },
        )
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                        // fix Notification permission in headless mode
                        Object.defineProperty(Notification, 'permission', { get: () => "default"});
                """
            },
        )
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                    Object.defineProperty(navigator, 'maxTouchPoints', {
                            get: () => 1
                    })"""
            },
        )
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                (function() {
                    const ORIGINAL_CANVAS = HTMLCanvasElement.prototype[name];
                    Object.defineProperty(HTMLCanvasElement.prototype, name, {
                            "value": function() {
                                    var shift = {
                                            'r': Math.floor(Math.random() * 10) - 5,
                                            'g': Math.floor(Math.random() * 10) - 5,
                                            'b': Math.floor(Math.random() * 10) - 5,
                                            'a': Math.floor(Math.random() * 10) - 5
                                    };
                                    var width = this.width,
                                            height = this.height,
                                            context = this.getContext("2d");
                                    var imageData = context.getImageData(0, 0, width, height);
                                    for (var i = 0; i < height; i++) {
                                            for (var j = 0; j < width; j++) {
                                                    var n = ((i * (width * 4)) + (j * 4));
                                                    imageData.data[n + 0] = imageData.data[n + 0] + shift.r;
                                                    imageData.data[n + 1] = imageData.data[n + 1] + shift.g;
                                                    imageData.data[n + 2] = imageData.data[n + 2] + shift.b;
                                                    imageData.data[n + 3] = imageData.data[n + 3] + shift.a;
                                            }
                                    }
                                    context.putImageData(imageData, 0, 0);
                                    return ORIGINAL_CANVAS.apply(this, arguments);
                            }
                    });
                })(this)
                """
            },
        )
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                    
                    Object.defineProperty(window, 'chrome', {
                        value: new Proxy(window.chrome, {
                                has: (target, key) => true,
                                get: (target, key) => {
                                        return {
                                                app: {
                                                        isInstalled: false,
                                                },
                                                webstore: {
                                                        onInstallStageChanged: {},
                                                        onDownloadProgress: {},
                                                },
                                                runtime: {
                                                        PlatformOs: {
                                                                MAC: 'mac',
                                                                WIN: 'win',
                                                                ANDROID: 'android',
                                                                CROS: 'cros',
                                                                LINUX: 'linux',
                                                                OPENBSD: 'openbsd',
                                                        },
                                                        PlatformArch: {
                                                                ARM: 'arm',
                                                                X86_32: 'x86-32',
                                                                X86_64: 'x86-64',
                                                        },
                                                        PlatformNaclArch: {
                                                                ARM: 'arm',
                                                                X86_32: 'x86-32',
                                                                X86_64: 'x86-64',
                                                        },
                                                        RequestUpdateCheckStatus: {
                                                                THROTTLED: 'throttled',
                                                                NO_UPDATE: 'no_update',
                                                                UPDATE_AVAILABLE: 'update_available',
                                                        },
                                                        OnInstalledReason: {
                                                                INSTALL: 'install',
                                                                UPDATE: 'update',
                                                                CHROME_UPDATE: 'chrome_update',
                                                                SHARED_MODULE_UPDATE: 'shared_module_update',
                                                        },
                                                        OnRestartRequiredReason: {
                                                                APP_UPDATE: 'app_update',
                                                                OS_UPDATE: 'os_update',
                                                                PERIODIC: 'periodic',
                                                        },
                                                },
                                        }
                                }
                        })
                    });
                    """
            },
        )
        driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
                            Object.defineProperty(navigator, 'maxTouchPoints', {
                                get: () => 1
                            })"""
            },
        )

    @staticmethod
    def random_cdc():
        cdc = random.choices(string.ascii_lowercase, k=26)
        cdc[-6:-4] = map(str.upper, cdc[-6:-4])
        cdc[2] = cdc[0]
        cdc[3] = "_"
        return "".join(cdc).encode()

    def patch_binary(self, chromedriver):
        linect = 0
        replacement = self.random_cdc()
        with io.open(chromedriver, "r+b") as fh:
            for line in iter(lambda: fh.readline(), b""):
                if b"cdc_" in line:
                    fh.seek(-len(line), 1)
                    newline = re.sub(b"cdc_.{22}", replacement, line)
                    fh.write(newline)
                    linect += 1
            return linect