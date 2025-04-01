#!/usr/bin/python
#coding: utf-8
#
#
import csv
import MeCab
import ipadic
import wordcloud


#
# ストップワードかどうか
#
def is_stopwords(surface, feature):
    
    feature_0_list = ['BOS/EOS','記号','助詞','助動詞','副詞','連体詞','代名詞','形容動詞','接続詞','形容詞','接頭詞']
    feature_1_list = ['自立','非自立','数','形容動詞語幹','代名詞','副詞可能','数接続']
    feature_2_list = ['助数詞']
    feature_4_list = ['一段']
    surface_K_list = ['赤','青','存','在','膝','的','約','話','便','比','品','街','口','さ','むの','ら','対','笑','足','人','趣','町','場','公',
                      '室','ァ','性','代','冠','土','東','只','面','論','音','配','化','あ','化','首','氏','資','点','下','別','間','側','早',
                      '上','等','道','市','姿','手','内','物','真','ー','つまり','がっ','一','さん','ーー','京','ン','誌','半','筋','否',
                      'うに','りこ','もと','がる','分','系','声','車','家','客','地','中','次','例','他','ha','そう','たち','わる','うち','つき',
                      'イス','煙突','代表取締役社長','現状','そのもの','きっかけ','初日','そば','響き','付近','中略','状態','状況','事例','適用',
                      '中心','頓着','周囲','好例','性質','数値','表面','方向性','ふつう','想像','長期','方針','針','穴','隙間','ケース','動き',
                      '向け','目安','背景','話題','各社','発行','記録','平均','嘆息','移動','人口','看板','目的','小誌','メイン','筆者','一連',
                      '取り組み','周辺','モノ','トー','くだん',
                      '最初','問い合わせ','お隣','住所','平均','回転','坪','玄関','スタッフ','やり方','持ち主','個々','事情']

    item = feature.split(',')

    if item[0] in feature_0_list:
      return True
    if item[1] in feature_1_list:
      return True
    if item[2] in feature_2_list:
      return True
    if item[4] in feature_4_list:
      return True
    if surface in surface_K_list:
      return True
    return False


#
# 形態素解析をした結果をcsvファイルで出力
# 単語をリターン
#
def get_parse(txt_path, csv_path):
  #テキストファイルの読み込み
  with open(txt_path) as f:
    text = f.read()

  #形態素解析
  mecab = MeCab.Tagger(ipadic.MECAB_ARGS + " -u user.dic") 
  nodes = mecab.parseToNode(text) 

  #出力
  wc_text = ''
  with open(csv_path, 'w', newline='') as csvfile:
    w = csv.writer(csvfile)
    while nodes:
      if is_stopwords(nodes.surface, nodes.feature) != True:
        wc_text = wc_text + nodes.surface + ' '
        l = [nodes.surface]
        l.extend(nodes.feature.split())
        w.writerow(l)
      nodes = nodes.next
  return wc_text


#
#Word Cloudで単語頻度を視覚化したものを出力
#
#
def get_wordcloud(wc_text, png_path):
  wc = wordcloud.WordCloud(
      width=998,
      height=668,
      font_path="./msgothic.ttc",
      background_color='white',
      max_words=2000,
      max_font_size=64
  )
  wc.generate(wc_text) 
  wc.to_file(png_path)



text_ari = get_parse('./中国が北海道を買っている.txt',         './中国が北海道を買っている.csv')
text_kaw = get_parse('./北海道ただいま中国人に売り出し中.txt', './北海道ただいま中国人に売り出し中.csv')
get_wordcloud(text_ari, './中国が北海道を買っている.png')
get_wordcloud(text_kaw, './北海道ただいま中国人に売り出し中.png')

