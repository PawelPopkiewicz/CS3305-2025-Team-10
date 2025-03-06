"""
Really primitive testing of the route
"""

import requests
import json

# URL of the route
url = 'http://localhost:5002/predictions'  # Replace with the correct URL if different

# Example JSON data to test the route (modify this based on the actual structure required by your route)
test_trips = [
  {
    "_id": {
      "$oid": "67a91801538170c283819c4a"
    },
    "trip_id": "4497_38961",
    "start_time": "21:00:00",
    "start_date": "20250209",
    "schedule_relationship": "SCHEDULED",
    "route_id": "4476_87338",
    "direction_id": 0,
    "vehicle_updates": [
      {
        "timestamp": "1739134948",
        "latitude": 51.8670044,
        "longitude": -8.45518112
      },
      {
        "timestamp": "1739135007",
        "latitude": 51.8690109,
        "longitude": -8.44638348
      },
      {
        "timestamp": "1739135064",
        "latitude": 51.8711472,
        "longitude": -8.43845367
      },
      {
        "timestamp": "1739135124",
        "latitude": 51.8738632,
        "longitude": -8.43964863
      },
      {
        "timestamp": "1739135211",
        "latitude": 51.8769722,
        "longitude": -8.44040871
      },
      {
        "timestamp": "1739135238",
        "latitude": 51.8776817,
        "longitude": -8.44225597
      },
      {
        "timestamp": "1739135305",
        "latitude": 51.8805313,
        "longitude": -8.44866371
      },
      {
        "timestamp": "1739135394",
        "latitude": 51.8836365,
        "longitude": -8.45735264
      },
      {
        "timestamp": "1739135423",
        "latitude": 51.8848038,
        "longitude": -8.46039391
      },
      {
        "timestamp": "1739135517",
        "latitude": 51.8893318,
        "longitude": -8.46897411
      },
      {
        "timestamp": "1739135576",
        "latitude": 51.891922,
        "longitude": -8.46810532
      },
      {
        "timestamp": "1739135607",
        "latitude": 51.8929558,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739135667",
        "latitude": 51.8948326,
        "longitude": -8.46897411
      },
      {
        "timestamp": "1739135722",
        "latitude": 51.8962593,
        "longitude": -8.47255802
      }
    ]
  },
  {
    "_id": {
      "$oid": "67a91801538170c283819c4b"
    },
    "trip_id": "4497_34856",
    "start_time": "21:20:00",
    "start_date": "20250209",
    "schedule_relationship": "SCHEDULED",
    "route_id": "4476_87336",
    "direction_id": 1,
    "vehicle_updates": [
      {
        "timestamp": "1739134717",
        "latitude": 51.9218864,
        "longitude": -8.49428082
      },
      {
        "timestamp": "1739135327",
        "latitude": 51.9218864,
        "longitude": -8.49428082
      },
      {
        "timestamp": "1739135935",
        "latitude": 51.9218864,
        "longitude": -8.49428082
      },
      {
        "timestamp": "1739136052",
        "latitude": 51.9207878,
        "longitude": -8.49047947
      },
      {
        "timestamp": "1739136084",
        "latitude": 51.9190407,
        "longitude": -8.49069595
      },
      {
        "timestamp": "1739136144",
        "latitude": 51.9165154,
        "longitude": -8.49167442
      },
      {
        "timestamp": "1739136231",
        "latitude": 51.9155464,
        "longitude": -8.48635197
      },
      {
        "timestamp": "1739136296",
        "latitude": 51.9145088,
        "longitude": -8.48103
      },
      {
        "timestamp": "1739136327",
        "latitude": 51.9154167,
        "longitude": -8.47809792
      },
      {
        "timestamp": "1739136388",
        "latitude": 51.9165802,
        "longitude": -8.47451305
      },
      {
        "timestamp": "1739136475",
        "latitude": 51.915287,
        "longitude": -8.47375298
      },
      {
        "timestamp": "1739136505",
        "latitude": 51.915287,
        "longitude": -8.47375298
      },
      {
        "timestamp": "1739136593",
        "latitude": 51.916256,
        "longitude": -8.47049522
      },
      {
        "timestamp": "1739136622",
        "latitude": 51.9148979,
        "longitude": -8.47006
      },
      {
        "timestamp": "1739136679",
        "latitude": 51.9092674,
        "longitude": -8.47342682
      },
      {
        "timestamp": "1739136774",
        "latitude": 51.9079742,
        "longitude": -8.47418785
      },
      {
        "timestamp": "1739136800",
        "latitude": 51.9062881,
        "longitude": -8.47429562
      },
      {
        "timestamp": "1739136867",
        "latitude": 51.9032478,
        "longitude": -8.4721241
      },
      {
        "timestamp": "1739136956",
        "latitude": 51.9012413,
        "longitude": -8.47016907
      },
      {
        "timestamp": "1739136986",
        "latitude": 51.9011765,
        "longitude": -8.47027779
      },
      {
        "timestamp": "1739137047",
        "latitude": 51.8996239,
        "longitude": -8.47082138
      },
      {
        "timestamp": "1739137108",
        "latitude": 51.8996239,
        "longitude": -8.47082138
      },
      {
        "timestamp": "1739137159",
        "latitude": 51.8996239,
        "longitude": -8.47082138
      },
      {
        "timestamp": "1739137219",
        "latitude": 51.8996239,
        "longitude": -8.47082138
      },
      {
        "timestamp": "1739137311",
        "latitude": 51.8996239,
        "longitude": -8.47082138
      },
      {
        "timestamp": "1739137341",
        "latitude": 51.8996239,
        "longitude": -8.47082138
      },
      {
        "timestamp": "1739137438",
        "latitude": 51.8982658,
        "longitude": -8.47549057
      },
      {
        "timestamp": "1739137461",
        "latitude": 51.8970337,
        "longitude": -8.47483921
      },
      {
        "timestamp": "1739137522",
        "latitude": 51.8965187,
        "longitude": -8.47462177
      },
      {
        "timestamp": "1739137583",
        "latitude": 51.8967743,
        "longitude": -8.4712553
      },
      {
        "timestamp": "1739137672",
        "latitude": 51.8964539,
        "longitude": -8.46593285
      },
      {
        "timestamp": "1739137701",
        "latitude": 51.8953514,
        "longitude": -8.46517277
      },
      {
        "timestamp": "1739137760",
        "latitude": 51.8929558,
        "longitude": -8.46615
      },
      {
        "timestamp": "1739137858",
        "latitude": 51.8877144,
        "longitude": -8.46691132
      },
      {
        "timestamp": "1739137879",
        "latitude": 51.8870049,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137945",
        "latitude": 51.8835068,
        "longitude": -8.46777916
      },
      {
        "timestamp": "1739138035",
        "latitude": 51.882473,
        "longitude": -8.47701073
      },
      {
        "timestamp": "1739138068",
        "latitude": 51.8826027,
        "longitude": -8.47777176
      },
      {
        "timestamp": "1739138151",
        "latitude": 51.8840256,
        "longitude": -8.48407078
      },
      {
        "timestamp": "1739138188",
        "latitude": 51.882473,
        "longitude": -8.48461437
      },
      {
        "timestamp": "1739138270",
        "latitude": 51.8784599,
        "longitude": -8.48450565
      },
      {
        "timestamp": "1739138331",
        "latitude": 51.8784599,
        "longitude": -8.48450565
      },
      {
        "timestamp": "1739138361",
        "latitude": 51.8784599,
        "longitude": -8.48450565
      },
      {
        "timestamp": "1739138424",
        "latitude": 51.8772926,
        "longitude": -8.48461437
      },
      {
        "timestamp": "1739138479",
        "latitude": 51.8734093,
        "longitude": -8.48624325
      },
      {
        "timestamp": "1739138547",
        "latitude": 51.8688164,
        "longitude": -8.49004459
      }
    ]
  },
  {
    "_id": {
      "$oid": "67a91801538170c283819c4c"
    },
    "trip_id": "4497_65538",
    "start_time": "20:20:00",
    "start_date": "20250209",
    "schedule_relationship": "SCHEDULED",
    "route_id": "4476_87350",
    "direction_id": 1,
    "vehicle_updates": [
      {
        "timestamp": "1739134943",
        "latitude": 51.8491402,
        "longitude": -8.48885
      },
      {
        "timestamp": "1739135003",
        "latitude": 51.8490753,
        "longitude": -8.48841572
      },
      {
        "timestamp": "1739135068",
        "latitude": 51.8492699,
        "longitude": -8.48819828
      },
      {
        "timestamp": "1739135125",
        "latitude": 51.8486862,
        "longitude": -8.48776436
      },
      {
        "timestamp": "1739135217",
        "latitude": 51.8515358,
        "longitude": -8.48548317
      },
      {
        "timestamp": "1739135240",
        "latitude": 51.8522453,
        "longitude": -8.48287582
      },
      {
        "timestamp": "1739135281",
        "latitude": 51.8516,
        "longitude": -8.48113918
      },
      {
        "timestamp": "1739135317",
        "latitude": 51.8486214,
        "longitude": -8.47722912
      },
      {
        "timestamp": "1739135515",
        "latitude": 51.8721161,
        "longitude": -8.47407913
      },
      {
        "timestamp": "1739135576",
        "latitude": 51.8741875,
        "longitude": -8.47006
      },
      {
        "timestamp": "1739135607",
        "latitude": 51.879364,
        "longitude": -8.46517277
      },
      {
        "timestamp": "1739135667",
        "latitude": 51.8890076,
        "longitude": -8.46310902
      },
      {
        "timestamp": "1739135718",
        "latitude": 51.8951569,
        "longitude": -8.46300125
      },
      {
        "timestamp": "1739135810",
        "latitude": 51.8974876,
        "longitude": -8.46473789
      },
      {
        "timestamp": "1739135840",
        "latitude": 51.8978119,
        "longitude": -8.46669292
      },
      {
        "timestamp": "1739135905",
        "latitude": 51.8989105,
        "longitude": -8.466259
      },
      {
        "timestamp": "1739135966",
        "latitude": 51.8989105,
        "longitude": -8.466259
      },
      {
        "timestamp": "1739136058",
        "latitude": 51.8991699,
        "longitude": -8.46615
      },
      {
        "timestamp": "1739136082",
        "latitude": 51.8991699,
        "longitude": -8.46615
      },
      {
        "timestamp": "1739136143",
        "latitude": 51.8991699,
        "longitude": -8.46615
      },
      {
        "timestamp": "1739136204",
        "latitude": 51.8991699,
        "longitude": -8.46615
      },
      {
        "timestamp": "1739136265",
        "latitude": 51.8991699,
        "longitude": -8.46615
      },
      {
        "timestamp": "1739136326",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739136386",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739136478",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739136508",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739136589",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739136620",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739136681",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739136772",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739136802",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739136863",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739136954",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739136985",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137046",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137106",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137167",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137228",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137309",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137339",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137431",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137451",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137522",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137583",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137674",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137704",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137766",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137857",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137887",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739137948",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739138029",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739138059",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739138151",
        "latitude": 51.8992348,
        "longitude": -8.46604156
      }
    ]
  },
  {
    "_id": {
      "$oid": "67a91801538170c283819c4d"
    },
    "trip_id": "4497_40327",
    "start_time": "21:00:00",
    "start_date": "20250209",
    "schedule_relationship": "SCHEDULED",
    "route_id": "4476_87338",
    "direction_id": 1,
    "vehicle_updates": [
      {
        "timestamp": "1739134944",
        "latitude": 51.8956757,
        "longitude": -8.46549892
      },
      {
        "timestamp": "1739135004",
        "latitude": 51.8940582,
        "longitude": -8.46539
      },
      {
        "timestamp": "1739135060",
        "latitude": 51.8911438,
        "longitude": -8.46875668
      },
      {
        "timestamp": "1739135123",
        "latitude": 51.8901749,
        "longitude": -8.4693
      },
      {
        "timestamp": "1739135217",
        "latitude": 51.8872604,
        "longitude": -8.46604156
      },
      {
        "timestamp": "1739135247",
        "latitude": 51.886097,
        "longitude": -8.46408653
      },
      {
        "timestamp": "1739135305",
        "latitude": 51.8837,
        "longitude": -8.45757
      },
      {
        "timestamp": "1739135390",
        "latitude": 51.880661,
        "longitude": -8.44931602
      },
      {
        "timestamp": "1739135426",
        "latitude": 51.8800774,
        "longitude": -8.44746876
      },
      {
        "timestamp": "1739135516",
        "latitude": 51.8772278,
        "longitude": -8.44106102
      },
      {
        "timestamp": "1739135569",
        "latitude": 51.8773575,
        "longitude": -8.43932343
      },
      {
        "timestamp": "1739135604",
        "latitude": 51.8738,
        "longitude": -8.43964863
      },
      {
        "timestamp": "1739135665",
        "latitude": 51.8707581,
        "longitude": -8.43888855
      },
      {
        "timestamp": "1739135728",
        "latitude": 51.8697853,
        "longitude": -8.44279861
      },
      {
        "timestamp": "1739135813",
        "latitude": 51.8674545,
        "longitude": -8.45116234
      },
      {
        "timestamp": "1739135840",
        "latitude": 51.8670044,
        "longitude": -8.45518112
      },
      {
        "timestamp": "1739135907",
        "latitude": 51.8668747,
        "longitude": -8.46234894
      }
    ]
  },
  {
    "_id": {
      "$oid": "67a91801538170c283819c4e"
    },
    "trip_id": "4497_62500",
    "start_time": "20:20:00",
    "start_date": "20250209",
    "schedule_relationship": "SCHEDULED",
    "route_id": "4476_87348",
    "direction_id": 1,
    "vehicle_updates": [
      {
        "timestamp": "1739134948",
        "latitude": 51.8910141,
        "longitude": -8.46386909
      },
      {
        "timestamp": "1739135006",
        "latitude": 51.89328,
        "longitude": -8.46582413
      },
      {
        "timestamp": "1739135067",
        "latitude": 51.89328,
        "longitude": -8.46582413
      },
      {
        "timestamp": "1739135123",
        "latitude": 51.8933449,
        "longitude": -8.46582413
      },
      {
        "timestamp": "1739135210",
        "latitude": 51.8943825,
        "longitude": -8.46680164
      },
      {
        "timestamp": "1739135248",
        "latitude": 51.895546,
        "longitude": -8.47223282
      },
      {
        "timestamp": "1739135305",
        "latitude": 51.8966446,
        "longitude": -8.47462177
      },
      {
        "timestamp": "1739135395",
        "latitude": 51.8966446,
        "longitude": -8.47462177
      },
      {
        "timestamp": "1739135426",
        "latitude": 51.8966446,
        "longitude": -8.47462177
      },
      {
        "timestamp": "1739135514",
        "latitude": 51.8978767,
        "longitude": -8.47646809
      },
      {
        "timestamp": "1739135576",
        "latitude": 51.8976822,
        "longitude": -8.47788
      },
      {
        "timestamp": "1739135600",
        "latitude": 51.8976173,
        "longitude": -8.47874928
      },
      {
        "timestamp": "1739135660",
        "latitude": 51.8974876,
        "longitude": -8.47994423
      },
      {
        "timestamp": "1739135722",
        "latitude": 51.8974876,
        "longitude": -8.47994423
      },
      {
        "timestamp": "1739135813",
        "latitude": 51.8974876,
        "longitude": -8.47994423
      },
      {
        "timestamp": "1739135843",
        "latitude": 51.8974876,
        "longitude": -8.47994423
      },
      {
        "timestamp": "1739135907",
        "latitude": 51.8965187,
        "longitude": -8.48450565
      },
      {
        "timestamp": "1739135963",
        "latitude": 51.8956757,
        "longitude": -8.48841572
      },
      {
        "timestamp": "1739136055",
        "latitude": 51.8950272,
        "longitude": -8.49265099
      },
      {
        "timestamp": "1739136086",
        "latitude": 51.8947678,
        "longitude": -8.4941721
      },
      {
        "timestamp": "1739136143",
        "latitude": 51.8942528,
        "longitude": -8.49699593
      },
      {
        "timestamp": "1739136232",
        "latitude": 51.8923111,
        "longitude": -8.50579262
      },
      {
        "timestamp": "1739136290",
        "latitude": 51.8911438,
        "longitude": -8.50644493
      },
      {
        "timestamp": "1739136325",
        "latitude": 51.8889427,
        "longitude": -8.50753117
      },
      {
        "timestamp": "1739136382",
        "latitude": 51.8885574,
        "longitude": -8.51296234
      },
      {
        "timestamp": "1739136469",
        "latitude": 51.8888779,
        "longitude": -8.52425671
      },
      {
        "timestamp": "1739136504",
        "latitude": 51.8888168,
        "longitude": -8.52697277
      },
      {
        "timestamp": "1739136597",
        "latitude": 51.8890724,
        "longitude": -8.53348923
      },
      {
        "timestamp": "1739136620",
        "latitude": 51.8891373,
        "longitude": -8.5339241
      },
      {
        "timestamp": "1739136684",
        "latitude": 51.8906937,
        "longitude": -8.53968
      },
      {
        "timestamp": "1739136776",
        "latitude": 51.8921165,
        "longitude": -8.55119324
      },
      {
        "timestamp": "1739136806",
        "latitude": 51.8922462,
        "longitude": -8.55879593
      },
      {
        "timestamp": "1739136859",
        "latitude": 51.8921814,
        "longitude": -8.56205368
      },
      {
        "timestamp": "1739136949",
        "latitude": 51.8899155,
        "longitude": -8.57411
      },
      {
        "timestamp": "1739136984",
        "latitude": 51.8896561,
        "longitude": -8.5771513
      },
      {
        "timestamp": "1739137039",
        "latitude": 51.8887482,
        "longitude": -8.58290672
      },
      {
        "timestamp": "1739137099",
        "latitude": 51.8881035,
        "longitude": -8.58812141
      },
      {
        "timestamp": "1739137164",
        "latitude": 51.8880386,
        "longitude": -8.5927906
      },
      {
        "timestamp": "1739137227",
        "latitude": 51.8877792,
        "longitude": -8.59887314
      },
      {
        "timestamp": "1739137318",
        "latitude": 51.8859673,
        "longitude": -8.60984325
      },
      {
        "timestamp": "1739137345",
        "latitude": 51.8857727,
        "longitude": -8.61701107
      },
      {
        "timestamp": "1739137429",
        "latitude": 51.8816948,
        "longitude": -8.62689495
      },
      {
        "timestamp": "1739137459",
        "latitude": 51.8816948,
        "longitude": -8.62689495
      },
      {
        "timestamp": "1739137523",
        "latitude": 51.8803368,
        "longitude": -8.63634396
      },
      {
        "timestamp": "1739137586",
        "latitude": 51.8745117,
        "longitude": -8.63341141
      },
      {
        "timestamp": "1739137677",
        "latitude": 51.8759346,
        "longitude": -8.6463356
      }
    ]
  }
        ]

for trip_data in test_trips:
    trip_data = trip_data["vehicle_updates"][:len(trip_data["vehicle_updates"]) // 2]

    # Send POST request to the Flask server
    response = requests.post(url, json=trip_data)

    # Print status code and response body
    if response.status_code == 200:
        print("Prediction successful")
        print(f"Response JSON: {response.json()}")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response Body: {response.text}")
