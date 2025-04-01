#!/usr/bin/python
#coding: utf-8
#
#
import csv
import MeCab
import ipadic


#
# 形態素解析をした結果をcsvファイルで出力
# 単語をリターン
#
def get_parse(txt_path, csv_path):
  #テキストファイルの読み込み
  with open(txt_path) as f:
    text = f.read()
  #形態素解析
  mecab = MeCab.Tagger(ipadic.MECAB_ARGS + " -u dice.dic") 
  nodes = mecab.parseToNode(text) 
  #出力
  wc_text = ''
  with open(csv_path, 'w', newline='') as csvfile:
    w = csv.writer(csvfile)
    while nodes:
      wc_text = wc_text + nodes.surface + ' '
      l = [nodes.surface]
      l.extend(nodes.feature.split())
      w.writerow(l)
      nodes = nodes.next
  return wc_text


#
# ダイス係数
#
#
def dice_coefficient(set_a, set_k):
    print(len(set_a.intersection(set_k)))
    i = len(set_a.intersection(set_k))
    return 2 * i / (len(set_a) + len(set_k))

text_ari = get_parse('./中国が北海道を買っている.txt',         './中国が北海道を買っている.csv')
text_kaw = get_parse('./北海道ただいま中国人に売り出し中.txt', './北海道ただいま中国人に売り出し中.csv')

set_ari = set(text_ari.split())
set_kaw = set(text_kaw.split())
print(dice_coefficient(set_ari, set_kaw))
