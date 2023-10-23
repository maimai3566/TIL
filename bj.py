# %% [markdown]ブラックジャック(Gitの練習です！)
# # ブラックジャック
# * プレイヤーとディーラーの1vs1で対戦
# * 配られたカードの合計が21に近いほうが勝ち（21を超えると負け確定）
# * カードのポイントは以下の通り  
#     * エース・・・1か11  
#     * 2～10・・・数字の通り  
#     * 11～13・・・10  
# * ルール
#     * プレイヤーが掛け金（bet）を決められる
#     * ゲームに勝つと掛け金の2倍を貰える。負けると没収
#     * 21で勝つとさらに1.5倍貰える
#     * 引き分けの場合は掛け金がそのまま戻される
# * ゲームの流れ
#     * 最初に掛金（bet）をプレイヤーが決める
#     * プレイヤーとディーラーそれぞれに2枚ずつカードが配布される
#     * ディーラーのカードは1枚だけ見えている状態
#     * プレイヤーターン
#         * スタンド(この手で勝負)
#         * ヒット（もう1枚）→21を超えるとバスト
#         * ダブル（ベットした金額を2倍にして勝負）
#         * バースト（負け確）
#     * ディーラーターン
#         * 手札が17以上のとき・・・スタンド
#         * 手札が17に満たない・・・ヒット→21を超えるとバスト
#     * ディーラーの手札をオープンし、勝負

# %%【関数】デッキを作る関数
import random
def make_deck():
    suits=['S','D','H','C']
    ranks=range(1,14)
    deck=[]
    deck=[(rank,suit) for rank in ranks for suit in suits]  #52枚のカードを作る
    random.shuffle(deck)    #シャッフル
    return deck

# %%手札を表示する関数
def print_hand(hand):
    for card in hand:
        print('[{} {}]'.format(card[1],card[0]))

# %%【関数】カードの点数を計算
def calk_point(hand):
    point=0 #初期化
    #カードを降順にしてからポイント計算（1を最後に計算したい）
    for card in sorted(hand,reverse=True):
        ten=card[0]
        if ten>10:
            point+=10
        elif ten>=2 and ten<=10:
            point+=ten
        elif ten==1:
            if point<10:
                point+=11
            else:
                point+=1
    return point

# %%【関数】判定と精算
def hantei(p_point,d_point,bet,p_money):
    if p_point>21:
        if d_point>21:
            #プレイヤー、ディーラーともにバースト
            print('プレイヤー{}点'.format(p_point)+' ディーラー{}点'.format(d_point)+' 【二人ともバースト】')
        else:
            #プレイヤーバースト
            print('プレイヤー{}点'.format(p_point)+' ディーラー{}点'.format(d_point)+' 【プレイヤーバースト負け】')
            bet=0
    elif p_point==d_point:
        #引き分け
        print('プレイヤー{}点'.format(p_point)+' ディーラー{}点'.format(d_point)+' 【引き分け】')
    elif p_point<d_point:
        if d_point>21:
            #ディーラーバースト
            print('プレイヤー{}点'.format(p_point)+' ディーラー{}点'.format(d_point)+' 【プレイヤーの勝ち】')
            bet*=2
        else:
            #負け
            print('プレイヤー{}点'.format(p_point)+' ディーラー{}点'.format(d_point)+' 【プレイヤーの負け】')
            bet=0
    elif p_point>d_point:
        if p_point==21:
            print('プレイヤー{}点'.format(p_point)+' ディーラー{}点'.format(d_point)+' 【プレイヤーブラックジャック！】')
            bet*=2.5
        else:
            print('プレイヤー{}点'.format(p_point)+' ディーラー{}点'.format(d_point)+' 【プレイヤーの勝ち】')
            bet*=2
    p_money+=bet
    return p_money

# %%プレイヤーのターン
def p_turn(deck,p_hand,bet,p_money):
    while True:
        try:
            ans=int(input('選択してね。スタンド＝1　ヒット＝2　ダブル＝3'))
            if ans==1:
                print('スタンド')
                break
            elif ans==2:
                print('ヒット')
                #カードを引く
                p_hand.append(deck.pop())
                #カードを引いたら表示
                print_hand(p_hand)
                #ポイントを計算し、21超過だったらターン終了
                p_point=calk_point(p_hand)
                if p_point>21:
                    break
            elif ans==3:
                print('ダブル')
                p_money-=bet
                bet*=2
                p_hand.append(deck.pop())
                print_hand(p_hand)
                break
            else:
                print('1、2、3以外の数字は入れないで！！！！')
                continue
        except: #文字列を入れたときの処理
            print('1、2、3以外の数字は入れないで！！！！')
            continue
    return bet,p_money


# %%ディーラーのターン
def d_turn(deck,d_hand):
    while True:
        d_point=calk_point(d_hand)
        if d_point>=17:
            break
        elif d_point<17:
            d_hand.append(deck.pop())
    return d_point

# %%メイン
#変数初期化
turn=0
p_money=100

#所持金が0円より大きければゲーム続行できる
while(p_money>0):
    #ターン
    turn+=1
    print('【{}ターン目】所持金＝{}'.format(turn,p_money))
    #デッキを作る
    deck=make_deck()

    p_hand,d_hand=[],[]
    p_point,d_point=0,0

    #ベットする
    while True:
        try:
            bet=int(input('ベットしてね💛'))
            #ベットが所持金より多かったらループ
            if bet>p_money:
                print('所持金{}より多くベットできないから！'.format(bet))
                continue
            break
        except:
            print('betは数字でないとダメだよ！')
            continue
    #所持金減らす
    p_money-=bet

    #プレイヤーカードを2枚引く
    p_hand=[deck.pop() for x in range(2)]
    #プレイヤーのカードを表示
    print_hand(p_hand)

    #ディーラーのカードを2枚引く
    d_hand.append(deck.pop())
    print('ディーラーのカード')
    print_hand(d_hand)  #1枚だけ表示
    d_hand.append(deck.pop())
    print('[* *]')

    #プレイヤーのターン（行動を決める）
    print('■プレイヤー------------------')
    bet,p_money=p_turn(deck,p_hand,bet,p_money)
    p_point=calk_point(p_hand)
    print('{}ポイント'.format(p_point))

    #ディーラーのターン
    print('■ディーラー------------------')
    d_turn(deck,d_hand)
    d_point=calk_point(d_hand)
    print_hand(d_hand)
    print('{}ポイント'.format(d_point))
    print('-----------------------------------')

    #勝負！
    p_money=hantei(p_point,d_point,bet,p_money)
    print('現在のマネー{}'.format(p_money))

    #勝負を続けるかどうかの確認
    ans=input('ゲームを続ける場合は[Y]、辞める場合は[N]を入力してください。Y/N？')
    if ans.lower()=='y':
        continue
    else:
        print('ゲームを終了します。あなたの所持金は{}円です♪またゲームしてね💛'.format(p_money))
        break
