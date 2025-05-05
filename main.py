from func import AccountMaker, Config

#account_num = int(input("Number of accounts: "))
#count = 0

#while account_num > count:
#    account_maker = AccountMaker(proxy=get_random_proxy())
#    account_maker.run()
    
config = Config("config.yml")

a = AccountMaker(config.get_random_proxy())
a.run(config)
