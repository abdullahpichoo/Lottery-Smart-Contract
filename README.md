# Lottery-Smart-Contract

- Users can enter the lottery based on an entrance fee
- An admin will start lottrey and he will end it (this must be changed to random start later)
- Lottrey will choose a random winner

- rn you're working with VRFConsumerV1 and remember to test for V2 as well

# How to test

- start with `mainnet-fork` as I'm working with onchain aggv3
- then I'll work with `development` network for function testing with mocks
- finally I'll test on `testnet`

# Testing

- Unit Tests: tests conducted on local development blockchain in which we test small pieces of code like individual functions. This makes sure every functions is behaving properly.
- Integration Tests: In this, we test multiple functions at once to test their working and are usually on Testnets after we have successfuly conducted our unit tests.
