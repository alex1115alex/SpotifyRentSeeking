import speech_recognition as sr
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By as by
import time, requests, os, shutil
from pydub import AudioSegment

def speech_to_text(filename) -> any:
    sound: AudioSegment = AudioSegment.from_mp3(filename)
    sound.export(filename.replace("mp3", "wav"), format="wav")
    r = sr.Recognizer()
    with sr.AudioFile(filename.replace("mp3", "wav")) as source:
        return r.recognize_google(r.record(source))

def solve(driver, i):
    frames = driver.find_elements(by.TAG_NAME, "iframe")
    # frames[0].click()
    time.sleep(7.5)
    for frame in frames:
        try:
            driver.switch_to.frame(frame)
            if driver.find_element(by.XPATH, "//button[@title='Get an audio challenge']").is_displayed():
                driver.find_element(by.XPATH, "//button[@title='Get an audio challenge']").click()
                time.sleep(2)
                if not os.path.exists(f"data/audio{i}"):
                    os.makedirs(f"data/audio{i}")
                open(f"data/audio{i}/audio_{i}.mp3", "wb").write(requests.get(driver.find_element(by.TAG_NAME, "a").get_attribute("href")).content)
                break
        except NoSuchElementException:
            driver.switch_to.default_content()
            pass
        except ElementNotInteractableException:
            pass
        except Exception as e:
            print(e)
    driver.switch_to.default_content()
    try: text = speech_to_text(f"data/audio{i}/audio_{i}.mp3"); print(text)
    except Exception as e: print(e)
    for frame in frames:
        try:
            driver.switch_to.frame(frame)
            if driver.find_element(by.XPATH, "//input[@type='text']").is_displayed():
                inpt = driver.find_element(by.XPATH, "//input[@type='text']")
                inpt.click()
                inpt.send_keys(text)
                time.sleep(2)
                driver.find_element(by.XPATH, "//button[@id='recaptcha-verify-button']").click()
                time.sleep(1.5)
                break
        except NoSuchElementException:
            driver.switch_to.default_content()
            pass
        except ElementNotInteractableException:
            pass
        except Exception as e:
            print(e)
    driver.switch_to.default_content()
    for frame in frames:
        try:
            driver.switch_to.frame(frame)
            if driver.find_element(by.XPATH, "//div[@class='recaptcha-checkbox-checkmark']").is_displayed():
                print("Done")
                break
        except NoSuchElementException:
            driver.switch_to.default_content()
            pass
        except Exception as e:
            print(e)
    driver.switch_to.default_content()
    shutil.rmtree(f"data/audio{i}")