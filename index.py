from flask import Flask, render_template, request

import firebase_admin

from firebase_admin import credentials, firestore

import os

import json



# 初始化 Flask 應用

app = Flask(__name__)



# 首頁路由

@app.route("/")

def home():

	return render_template("index.html")



# 老師查詢路由

@app.route("/search", methods=["GET", "POST"])

def search_teacher():

	result = []

	keyword = ""


	if request.method == "POST":

# 獲取使用者輸入的關鍵字

		keyword = request.form.get("keyword", "").strip()


# 連接 Firebase Firestore

		db = firestore.client()

# 讀取「靜宜資管」集合的所有文件

		docs = db.collection("靜宜資管").get()


# 遍歷所有文件，比對名字

		for doc in docs:

			teacher = doc.to_dict()

# 不區分大小寫比對，避免匹配失敗

			if keyword.lower() in teacher.get("name", "").lower():

				result.append(teacher)


# 渲染查詢頁面，傳入結果

	return render_template("search.html", keyword=keyword, results=result)



# Firebase 初始化（完美兼容本地 + Vercel 環境）

if not firebase_admin._apps:

	try:

# 本地環境：讀取 JSON 金鑰檔

		if os.path.exists("serviceAccountKey.json"):

			cred = credentials.Certificate("serviceAccountKey.json")

# Vercel 環境：讀取環境變數

		else:

			service_account_str = os.environ.get("SERVICE_ACCOUNT_KEY")

			if not service_account_str:

				raise ValueError("❌ SERVICE_ACCOUNT_KEY 環境變數未設定")

# 正確解析 JSON 字串

			cred = credentials.Certificate(json.loads(service_account_str))

# 初始化 Firebase

		firebase_admin.initialize_app(cred)

	except Exception as e:

		print(f"❌ Firebase 初始化失敗: {str(e)}")

		raise



# Flask 程式入口（Vercel 必須要有這個！）

if __name__ == "__main__":

	app.run(debug=True, host="0.0.0.0", port=5000)