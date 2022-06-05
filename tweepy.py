import tweepy


consumer_key = 'OJHdzWPwLDiZUMfR9QCOVJ3S7'
consumer_secret = 'KHU0JFbjSb96ct7wRiYk8Jf4vOhOp2SWC3pXdl2JPndIPJTYzc'

access_token = '2509564212-B3wia1Fpc1t78JYGHf4MsgIlqNfUayQUGAT9jrP'
access_token_secret = '4JwmO0gvkvJF1TXB5CEmvJAQwxLeAfPJS6ASSFEITVdhv'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


