from api_gateway import call_api

subscriberNo = 1
month = 2
year = 2027

print("🧾 [1] QUERY BILL")
res1 = call_api("query_bill", {
    "subscriberNo": subscriberNo,
    "month": month,
    "year": year
})
print(res1)

print("\n📄 [2] QUERY DETAILED BILL")
res2 = call_api("query_detailed_bill", {
    "subscriberNo": subscriberNo,
    "month": month,
    "year": year,
    "pageNumber": 1,
    "pageSize": 10
})
print(res2)

print("\n💳 [3] MAKE PAYMENT")
res3 = call_api("make_payment", {
    "subscriberNo": subscriberNo,
    "month": month,
    "year": year
})
print(res3)

print("\n🔁 [4] RE-CHECK QUERY BILL")
res4 = call_api("query_bill", {
    "subscriberNo": subscriberNo,
    "month": month,
    "year": year
})
print(res4)
