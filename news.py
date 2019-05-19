#!/usr/bin/env python3
# -*- coding: utf-8 -*-ZZ

import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from ipdb import set_trace
import parser as parser
from datetime import datetime

OUTPUT_FILE = './static/test.mp3'
OUTPUT_EXT = os.path.splitext(OUTPUT_FILE)[1][1:].lower()


class AITalkWebAPI:
	"""AITalk WebAPIを扱うクラス"""

	URL = 'https://webapi.aitalk.jp/webapi/v2/ttsget.php'	# WebAPI URL

	#  【通知されたものを指定してください】
	ID = '********'	# ユーザ名(接続ID)
	PW = '********'	# パスワード(接続パスワード)


	def __init__(self):
		"""コンストラクタ"""
		# 合成パラメータ（詳細はWebAPI仕様書を参照）
		self.username = self.ID
		self.password = self.PW
		self.speaker_name 	= 'nozomi_emo'	# 話者名
		self.style 			= '{"j":"1.0"}'	# 感情パラメータ
		self.input_type 	= 'text'		# 合成文字種別
		self.text 			= ''			# 合成文字
		self.volume 		= 1.0			# 音量（0.01-2.00）
		self.speed 			= 0.8			# 話速（0.50-4.00）
		self.pitch 			= 1.0			# ピッチ（0.50-2.00）
		self.range 			= 1.0			# 抑揚（0.00-2.00）
		self.output_type 	= 'sound'		# 出力形式
		self.ext 			= 'mp3'			# 出力音声形式

		# 合成結果データ
		self._headers = None
		self._sound = None
		self._err_msg = None


	def synth(self):
		"""
		音声合成
		@return 正常終了か
		"""
		# 合成パラメータを辞書化
		dic_param = {
			'username'		: self.username,
			'password'		: self.password,
			'speaker_name'	: self.speaker_name,
			'style'			: self.style,
			'input_type'	: self.input_type,
			'text'			: self.text,
			'volume'		: self.volume,
			'speed'			: self.speed,
			'pitch'			: self.pitch,
			'range'			: self.range,
			'output_type'	: self.output_type,
			'ext'			: self.ext,
		}

		# URLエンコードされた合成パラメータの生成
		encoded_param = urllib.parse.urlencode(dic_param).encode('ascii')
		# HTTPヘッダーの生成
		header = {'Content-Type': 'application/x-www-form-urlencoded',}
		# URLリクエストの生成
		req = urllib.request.Request(self.URL, encoded_param, header)

		ret = False
		try:
			# URL接続
			with urllib.request.urlopen(req) as response:
				# HTTPステータスコード、ヘッダー、音声データの取得
				self.code = response.getcode()
				self.headers = response.info()
				self.sound = response.read()
				ret = self.code == 200
		except urllib.error.HTTPError as e:
			self._err_msg = 'HTTPError, Code: ' + str(e.code) + ', ' + e.reason
		except urllib.error.URLError as e:
			self._err_msg = e.reason
		return ret


	def get_error(self):
		"""
		合成エラーメッセージの取得
		@return 合成エラーメッセージ
		"""
		return self._err_msg if self._err_msg is not None else ''


	def save_to_file(self, output_filepath):
		"""
		音声データのファイル出力
		@param output_filepath 出力ファイルパス
		@return 正常終了か
		"""
		if self.sound is None:
			return False

		try:
			with open(output_filepath, 'wb') as f:
				f.write(self.sound)
		except IOError as e:
			return False
		return True


def main(list_keywd):
	"""メイン処理"""

	# (1) 合成内容設定
	target_text = parser.get_text(list_keywd)
	target_text = target_text[:1000]
	current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
	target_file = 'music/' + current_time + '.mp3'	# mp3, ogg, m4a, wav いずれかのファイルパス

	# 出力ファイルから出力形式を決定
	ext = os.path.splitext(target_file)[1][1:]
	if ext == 'm4a':	# m4a拡張子はaacと設定
		ext = 'aac'

	# (2) AITalkWebAPIを使うためのインスタンス作成
	aitalk = AITalkWebAPI()

	# (3) インスタンスに指定したいパラメータをセット
	aitalk.text = target_text
	aitalk.username = 'spajam2019'
	aitalk.password = 'LTMd8Ep8'
	# aitalk.speaker_name = 'nozomi_emo'
	# aitalk.style = '{"j":"1.0"}'
	aitalk.ext = ext

	# (4) 合成
	if not aitalk.synth():
		# エラー処理
		print(aitalk.get_error(), file=sys.stderr)
		return 0

	# (5) ファイル保存
	if not aitalk.save_to_file(target_file):
		print('failed to save', file=sys.stderr)
		return 1
	return target_file
