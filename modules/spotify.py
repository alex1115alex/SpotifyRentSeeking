links = dict(
    default = "https://open.spotify.com/playlist/0Uqkud5bT23h1ojtREu01d",
    loginPage = 'https://accounts.spotify.com/en/login'
)


xpaths = dict(
    login_btn =    '//button[contains(text(), "Log in")]',
    loginButton =  "//button[@id='login-button']", #Mine
    user_form =    '//*[@id="login-username"]',
    pass_form =    "//*[@id='login-password']",
    weirdButton =  "//*[@data-testid='web-player-link']",
    playButton =   "//*[data-testid='play-button']",
    closeButton =  "//*[aria-label='Close']",

    cookie_check = "/html/body/div[1]/div[2]/div/form/div[3]/div[1]/div/label/span",
    submit_btn =   "//*[@id='login-button']",
    shuffle_btn =  "/html/body/div[4]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[1]/button[1]",
    repeat_btn =   "/html/body/div[4]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[2]/button[2]",
    play_btn =     "/html/body/div[4]/div/div[2]/div[3]/main/div[2]/div[2]/div/div/div[2]/section/div[3]/div/button[1]",
    song_name =    "/html/body/div[4]/div/div[2]/div[2]/footer/div/div[1]/div/div[2]/div[1]/div/div/div/div/span/a",
    time_track =   "/html/body/div[4]/div/div[2]/div[2]/footer/div/div[2]/div/div[2]/div[3]",
    skip_btn =     "/html/body/div[4]/div/div[2]/div[2]/footer/div/div[2]/div/div[1]/div[2]/button[1]"
)
