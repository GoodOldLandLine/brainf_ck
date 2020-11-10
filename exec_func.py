#brainf*ck実行関数 utf-8対応！

import re

MAX_BYTES = 30000 #仕様では3万以上必要らしい
MAX_LOOPS = 100000 #最大実行回数
COMMANDS = """
> ポインタを１進める
< ポインタを１戻す
+ ポインタの指す要素の値を１増やす
- ポインタの指す要素の値を１減らす
. ポインタの指す要素の値を外に出力
, 外から値を入力して、 ポインタの指す場所へ入れる
[ ポインタの指す要素の値が 0 だったら対応する次の ] までジャンプ
] ポインタの指す要素の値が 0 以外だったら対応する前の [ までジャンプ
"""
def set_max_loops(n):
    global MAX_LOOPS
    MAX_LOOPS = n


class Memory():
    """
    バイト配列とポインターを管理する
    """
    def __init__(self, prohibited_overflow = False):
        """
        Parameters
        --------------
        prohibited_overflow : bool
        オーバーフローまたはアンダーフロー
        を検知して例外を投げる
        """
        #バイト配列は生成時に0x00で初期化される
        self.b = bytearray(MAX_BYTES)
        self.p = 0
        self.prohibited_overflow = prohibited_overflow
    
    def next_p(self):
        """
        ポインターを1つ進める
        """
        self.p += 1
    
    def back_p(self):
        """
        ポインターを1つ戻す
        """
        self.p -= 1
    
    def inc(self):
        """
        ポインターの指す要素の値を1増やす
        オーバーフローしたら0x00にする
        """
        self.__check_index_range()
        if self.b[self.p] == 0xff:
            if self.prohibited_overflow:
                raise OverflowError(
                "memory was called inc at index {}"
                " but overflowed".format(self.p))
            else:
                self.b[self.p] = 0x00
        else:
            self.b[self.p] += 0x01
        
    def dec(self):
        """
        ポインターの指す要素の値を1減らす
        アンダーフローしたら0xffにする
        """
        self.__check_index_range()
        if self.b[self.p] == 0x00:
            if self.prohibited_overflow:
                raise OverflowError(
                "memory was called dec at index {}"
                " but overflowed".format(self.p))
            else:
                self.b[self.p] = 0xff
        else:
            self.b[self.p] -= 0x01
    
    def read(self):
        """
        ポインターの指す要素を整数値で返す
        """
        self.__check_index_range()
        return int(self.b[self.p])
    
    def write(self, n):
        """
        ポインターの指す要素に整数値を代入する
        """
        self.__check_index_range()
        self.b[self.p] = n
    
    def __check_index_range(self):
        """
        メモリ領域外アクセスを検知して例外を投げる
        """
        if self.p < 0 or MAX_BYTES <= self.p:
            raise IndexError(
                "memory's index must be in range(0, {})"
                " but index was {}".format(MAX_BYTES, self.p))

            
def execute(exec_code
            , input_code=""
            , console_mode=False
            , prohibited_overflow = False
            , output_as_bytecode = False):
    """
    brainf*ckを実行する
    
    Parameters
    -------------
    exec_code: str
    実行コード
    input_code: str
    入力コード(任意)
    console_mode: bool
    input_codeが終端に達した後の
    入力をコンソールからの手動の入力とする
    """
    #入力コードを整数値で1個ずつ取得するためのジェネレーター
    get_int = (b for b in input_code.encode())
    #出力用バッファー
    output_buff = bytearray(0)
    #メモリの準備
    memory = Memory(
        prohibited_overflow=prohibited_overflow)
    #'<>+-.,'用の操作を格納
    simple_operations = { 
        '>': memory.next_p, 
        '<': memory.back_p,
        '+': memory.inc,
        '-': memory.dec,
        #出力用バッファーに読み取った整数値を格納する
        '.': lambda: [output_buff.append(memory.read())],
    }
    
    #読み取る実行コードのインデックス
    n = 0
    try:
        for i in range(MAX_LOOPS):
            #実行コードを読み取り終端に達したらbreakする
            try:
                command = exec_code[n]
            except IndexError as e:
                print("code length is {}. {} steps".format(n, i))
                break

            #実行コード通りに実行
            if command in "<>+-.":
                simple_operations[command]()
            elif command == ',':
            #ポインターの示す要素に入力値を代入する
                try:
                    memory.write(next(get_int))
                except StopIteration:
                    #入力が終端に達したらEOF=0xffを入力とし、
                    #それ以降は0x00を入力とする
                    if console_mode:
                        get_int = (b for b in input().encode())
                    else:
                        memory.write(0xff)
                        get_int = (0x00 for i in range(MAX_LOOPS))

            elif (command == '[') and (memory.read() == 0x00):
                brackets = 1 #[で+1 ]で-1
                while(brackets != 0):
                    #対応する]までnを進める
                    try:
                        n += 1
                        if exec_code[n] == '[':
                            brackets += 1
                        elif exec_code[n] == ']':
                            brackets -= 1
                    except IndexError as e:
                        raise e("missing one or more ']' ")
            elif (command == ']') and (memory.read() != 0x00):
                brackets = -1 #[で+1 ]で-1
                while(brackets != 0):
                    #対応する[までnを戻す
                    try:
                        n -= 1
                        if exec_code[n] == '[':
                            brackets += 1
                        elif exec_code[n] == ']':
                            brackets -= 1
                    except IndexError as e:
                        raise e("missing one or more '['")
            n += 1
        else:
            print("finish because loop count exceeded upper limit.")
    except Exception as e:
        print(f"\nBrainf*ck execute traceback:\n"
              f"{exec_code[n-100:n]}\n\n"
              f"THIS {exec_code[n]} !!!!\n\n{exec_code[n+1:n+100]}")
        raise e
    if output_as_bytecode:
         print(output_buff)
    else:
        print(output_buff.decode(errors='replace'))


def cut_non_recog(exec_code):
    """
    認識されない文字列をカットする
    
    Parameters
    -------------
    exec_code: str
    
    Returns
    -------------
    cut_code: str
    """
    not_required = r"[^\[\]\+\-<>\.,]"
    cut_code = re.sub(not_required, r'', exec_code)
    return cut_code


def cut_pair(exec_code):
    """
    <>や><、+-、-+のペアを無くす
    
    Parameters
    -------------
    exec_code: str
    
    Returns
    -------------
    cut_code: str
    """
    inc_dec_pair = re.compile(r"<>|><|\+\-|\-\+")
    cut_code = exec_code
    
    cut_num = 1
    while(cut_num >= 1):
        cut_code, cut_num = re.subn(inc_dec_pair, r'', cut_code)
    return cut_code


def optimizer(exec_code):
    """
    実行コード最適化を行う
    
    Parameters
    --------------
    exec_code: str
    
    Returns
    --------------
    optimized_code: str
    """
    #最適化用関数　順序が大事!
    optimize_funcs = [
        cut_non_recog,
        cut_pair,
    ]
    
    optimized_code = exec_code
    for optimize_func in optimize_funcs:
        optimized_code = optimize_func(optimized_code)
    
    return optimized_code