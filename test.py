from moralis import evm_api

api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6IjQ0MmIzOTBkLWEzYzQtNDk4Yy1hMWIyLWFhMDNlMWEzOWJiMiIsIm9yZ0lkIjoiMzY3MDkwIiwidXNlcklkIjoiMzc3MjcwIiwidHlwZUlkIjoiMmU4MDE2ZTQtZDdmNC00YzE1LWJlYjctNTM3OGZmMjcxYTI2IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MDE4MzY0NTYsImV4cCI6NDg1NzU5NjQ1Nn0.IHTrP6HabjODpG7gHm6UMGukC312RYSbyxCmLkHTQIA"

params = {
  "chain": "bsc",
  "order": "DESC",
  "address": "0x3709f1B70592EBeBDbb47f7FF4Cdc54d69224A95"
}

result = evm_api.token.get_wallet_token_transfers(
  api_key=api_key,
  params=params,
)

print(result)

BSC_TRADER = [
    "0x3709f1b70592ebebdbb47f7ff4cdc54d69224a95",
    "0x0475c991adddfeda6705667ee9b54a95bc427fe4",
    "0xd2072a338017d2aac0ae736f04a57384425731f8",
    "0x1ce3a7c3b488ceab7ef3d1210b274979e699275b",
    "0x9ea981a8091f1355141b73e617d905155c228593",
    "0xdcac668b4c6049affe911cca3aaa490f8e20c9b6",
    "0x947acd01beb4c0ba3d5ea1bda473d40f0069adc5",
    "0x92bd2fa2f9000e75fa8f7b5afc5842725e33b43b",
    "0x83581d22d37d9c71febcf971905b6007a2c1fdd8",
    "0x2f6b6a88217a118b25fc1ae4bd08060ec21cb2ce"
]

ETH_TRADER = [
    "0x64c7e437abd780ceecbe4b1beef05c4746f61482",
    "0x28f9c9f9d97413d16a888f8f97373fd68b473028",
    "0x1a4dda045a0600504417f12d9e36c8b3f16b0beb",
    "0xc7b3c20c81f0fa4c96e846feb149658cfcd76448",
    "0xf13eec9b183021ed9465888276cd2d1390e42fad",
    "0x68c427b37e05feba97ffe415ddf5b378cab72ef6",
    "0x7ce3bfba3c77518a7081cd6cde037eae8c344fb5",
    "0xd2cf8ba2ccdb4b85392c3fff2869a16239fdae28",
    "0x2530d0b66e71b53d585ebeef2f6539d25d02cc76",
    "0x39d9366b8cc0b2dbbe1144b0c6e423bd64dde3e8"
]