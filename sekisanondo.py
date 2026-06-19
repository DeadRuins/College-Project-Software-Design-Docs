import csv

file_path = "temperature_log.csv"
temperatures = []

# CSVファイルを開く
with open(file_path, mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)  # ヘッダー名でデータにアクセスできる形式で読み込み

    for row in reader:
        # 文字列から浮動小数点数(double/float)に変換してリストに追加
        temp_value = float(row["Temperature (°C)"])
        temperatures.append(temp_value)

# 結果の確認
print("読み込んだ温度リスト（double型）:")
print(temperatures)
#print(f"データの型: {type(temperatures[0])}")

sekisanondo=0.0
for temperature in temperatures:
    sekisanondo = sekisanondo + temperature

print("積算温度:")
print(round(sekisanondo,1))
