# 使用可能なメモリの位置を格納する
available_mem = 0

class Var:
    """
    Varオブジェクトはインスタンス化された時点で
    自動的にメモリ上の特定の複数バイトと一対一に結び付けられ
    以後その対応関係は変更することができない
    """
    def __init__(self):
        global available_mem
        self.m = available_mem
        self.s1 = available_mem + 1
        self.s2 = available_mem + 2
        self.s3 = available_mem + 3
        available_mem += 4
   

    # 基底位置前提 ---------------------------    
    # 操作
    def copy(self, n):
        """
        メインバイトに代入する
        
        Parameters
        -----------
        n: int, Var
        代入する数　正の数またはゼロ
        またはVarオブジェクト
        
        Algorithm
        -----------
        m = 0
        m += n
        """
        return self.set_zero()+self.add(n)
    def set_zero(self):
        """
        メインバイトをゼロにする
        """
        return self.__inmyworld("[-]")
    # 算術演算
    def add(self, n):
        """
        加算
        
        Parameters
        ----------------
        n: int, Var
        加数　正の数またはゼロ
        またはVarオブジェクト
        """
        if type(n) is int:
            if n < 0:
                raise ValueError(f"n must be more than zero. but n is {n}")
            # メインバイトに加算
            return self.__inmyworld('+'*n)
        elif type(n) is Var:
            """
            Algorithm
            ----------
            m==x, s1==0, s2==0, s3==0, n==y
            s3 = n
            s3{
                m++
            }
            """
            # s3 = n
            code = self.__copyto_s3(n)
            # m+=s3, s3=0
            code += ">>>[-<<<+>>>]<<<"
            return self.__inmyworld(code)
        else:
            raise TypeError(f"type(n) must be int or Var but {type(n)}")
    def mul(self, n):
        """
        乗算
        
        Parameters
        ----------------
        n: int
        乗数　正の数またはゼロ
        または Var
        
        Algorithm
        ----------------
        m==x, s1==0, s2==0, s3==0
        s3+=n
        s3{
            m{
                s1++
                s2++
            }
            s1{
                m++
            }
        }
        m{}
        s2{
            m++
        }
        """
        # s3 = n
        if type(n) is int: 
            if n < 0:
                raise ValueError(f"n must be more than zero. but n is {n}")
            code = f">>>{'+'*n}<<<"
        elif type(n) is Var:
            code = self.__copyto_s3(n)
        else:
            raise TypeError(f"type(n) must be int or Var but {type(n)}")
        # s1 = 0, s2 = m * s3, s3 = 0
        code += ">>>[-<<<[->+>+<<]>[-<+>]>>]<<<"
        # m = 0
        code += "[-]"
        # m = s2, s2 = 0
        code += ">>[-<<+>>]<<"
        return self.__inmyworld(code)
    # 論理演算
    def tobool(self):
        """
        メインバイトが0の場合はそのまま
        そうでない場合は1に変換する
        
        Algorithm
        -------------
        m == x, s1==0
        m{
            m{}
            s1++
        }
        s1{m++}
        """
        # m=0; s1= 0 if m==0 else 1
        code = "[-[-]>+<]"
        # m=s1, s1=0
        code += ">[-<+>]<"
        return self.__inmyworld(code)
    def neg(self):
        """
        真理値反転
        
        Algorithm
        -----------
        s1++
        m{
            m{}
            s1--
        }
        s1{m}
        """
        # s1=1
        code = ">+<"
        # m=0, s1= 0 if m==0 else 1
        code += "[-[-]>-<]"
        # m=s1, s1=0
        code += ">[-<+>]<"
        return self.__inmyworld(code)
    def gt(self, n):
        """
        大小比較
        メインバイト>nを演算し結果を
        メインバイトに入れる。
        m = max(m-n, 0)の演算に等しい
        
        Parameters
        -------------
        n: int or Var
        
        Algorithm
        --------------
        m==x, s1==0, s2==0, s3==0, n==y
        s3 = n
        s3{
            m{
                s1++
                s2++
            }
            s2{
                m++
            }
            s2++
            s1{
                m--
                s2--
                s1{}
            }
            s2{
                s3{}
            }
        }
        """
        # s3 = n
        if type(n) is int: 
            if n < 0:
                raise ValueError(f"n must be more than zero. but n is {n}")
            code = f">>>{'+'*n}<<<"
        elif type(n) is Var:
            code = self.__copyto_s3(n)
        else:
            raise TypeError(f"type(n) must be int or Var but {type(n)}")
        # m = max(m-s3, 0), s3=0
        code += """
            >>>[-<<<
                [-
                    >+<
                    >>+<<
                ]
                >>[-<<
                    +
                >>]<<
                >>+<<
                >[-<
                    -
                    >>-<<
                    >[-]<
                >]<
                >>[-<<
                    >>>[-]<<<
                >>]<<
            >>>]<<<
        """
        return self.__inmyworld(code)
    def ge(self, n):
        """
        大小比較
        メインバイト>=nを演算し結果を
        メインバイトに入れる。
        一般にm,nが整数のとき
        m>=n <=> m+1>n
        であることを利用する。
        """
        return self.add(1)+self.gt(n)
    def lt(self, n):
        """
        大小比較
        メインバイト<nを演算し結果を
        メインバイトに入れる。
        geの結果の否定
        """
        return self.ge(n)+self.neg()
    def le(self, n):
        """
        m < n
        gtの結果の否定
        """
        return self.gt(n)+self.neg()
    def eq(self, n):
        """
        等価演算
        nと比較して等しければ非ゼロ
        等しくなければゼロを返す
        
        Parameters
        -------------
        n: int or Var
        
        Algorithm
        --------------
        gtを応用したもの
        m==x, s1==0, s2==0, s3==0, n==y
        s3 = n
        s3++          # 変更点その１
        s3{
            m{
                s1++
                s2++
            }
            s2{
                m++
            }
            s2++      # mがゼロならこのフラグが立ちっぱなし
            s1{
                m--
                s2--
                s1{}
            }
            s2{       # mがゼロなら実行
                      # mはこのループで一度も減算していないことに注意
                s1++  # 変更点その２ s3がゼロならこのフラグが立ちっぱなし
                s3{
                    s1--
                    s3{}
                }
            }
        }
        #以下変更点３
        m{}           # mにはmax(m-n, 0)が格納されるが0にする
        s1{
            m++
        }
        """
        # s3 = n
        if type(n) is int: 
            if n < 0:
                raise ValueError(f"n must be more than zero. but n is {n}")
            code = f">>>{'+'*n}<<<"
        elif type(n) is Var:
            code = self.__copyto_s3(n)
        else:
            raise TypeError(f"type(n) must be int or Var but {type(n)}")
        # s3 += 1
        code += ">>>+<<<"
        # m = max(m-s3, 0), s3=0, s1= 1 if m==n else 0
        code += """
            >>>[-<<<
                [-
                    >+<
                    >>+<<
                ]
                >>[-<<
                    +
                >>]<<
                >>+<<
                >[-<
                    -
                    >>-<<
                    >[-]<
                >]<
                >>[-<<
                    >+<
                    >>>[-<<<
                        >-<
                        >>>[-]<<<
                    >>>]<<<
                >>]<<
            >>>]<<<
        """
        # m=0
        code += "[-]"
        # m=s1, s1=0
        code += ">[-<+>]<"
        return self.__inmyworld(code)
    # 分岐
    def if_true(self, if_braces, else_braces):
        """
        メインバイトが非ゼロならif_bracesを実行し、
        メインバイトがゼロならelse_bracesを実行する
        
        Parameters
        ---------------
        if_braces: str
        有効な基底位置・非破壊設計のbrainf*ckコード
        else_braces: str
        有効な基底位置・非破壊設計のbrainf*ckコード
        
        Algorithm
        ---------------
        m==x, s1==0, s2==0, s3==0
        m{
            s1++
            s2++
        }
        s2{
            m++
        }
        s2++
        s1{
            outerCode1
            s1{}
            s2{}
        }
        s2{
            outerCode2
            s2{}
        }
        """
        # s1 = m
        code = "[->+>+<<]>>[-<<+>>]<<"
        # s2 = 1
        code += ">>+<<"
        # if braces
        code += f"""
            >[-<
                {self.__intheground(if_braces)}
                >[-]<
                >>[-]<<
            >]<
        """
        # else braces
        code += f"""
            >>[-<<
                {self.__intheground(else_braces)}
                >>[-]<<
            >>]<<
        """
        return self.__inmyworld(code)
    # 反復
    def while_n(self, braces):
        """
        メインバイトの値の回数だけbracesを実行する
        
        Parameters
        ------------
        braces: str
        有効な基底位置・非破壊なbrainf*ckコード
        
        Algorithm
        ------------
        m==x, s1==0, s2==0, s3==0
        m{
            s1++
            s2++
        }
        s2{
            m++
        }
        s1{
            outerCode
        }
        """
        # m=m, s1=m, s2=0, s3=0
        code = "[->+>+<<]>>[-<<+>>]<<"
        # exec outerCode for m times; s1=0
        code += ">[-<"
        code += self.__gotoG() + braces + self.__gotoM()
        code += ">]"
        
        return self.__inmyworld(code)
    def while_v(self, flag, braces):
        """
        flagがゼロになるまでbracesを実行する。
        flagはbraces内での操作が適用される。
        Parameters
        ------------
        falg: Var
        selfを除くVarオブジェクト
        braces: str
        有効な基底位置・非破壊なbrainf*ckコード
        
        Algorithm
        ------------
        m==x, s1==0, s2==0, s3==0, flag==x
        s3 = flag
        s3{
            outercode(flag can be changed)
            s3 = 0
            s3 = flag
        }
        """
        # s3=flag
        code = self.__copyto_s3(flag)
        # loop
        code += f"""
                >>>[-<<<
                    {self.__intheground(braces)}
                    >>>[-]<<<
                    {self.__copyto_s3(flag)}
                >>>]<<<
        """
        return self.__inmyworld(code)
        
    # 出力
    def show(self, b=False):
        """
        メインバイトを出力する
        
        Parameters
        -----------
        b: bool
        バイト値をunicodeの数字に変換する
        """
        if b:
            code = f"{'+'*ord('0')}.{'-'*ord('0')}"
        else:
            code = '.'
        return self.__inmyworld(code)
    def printstr(self, s):
        """
        サブバイトを利用して任意の文字列を出力する
        メインバイトは変化しない
        
        Parameters
        -----------
        s: str
        
        Algorithms
        -----------
        Example printstr("hello")
        m==x,s1==0
        s1 = ord('h')
        show s1
        s1 = ord('e')
        ...
        """
        code = ""
        for n in s.encode():
            code += f">{'+'*n}.[-]<"
        return self.__inmyworld(code)
    # 入力
    def getchar(self):
        """
        入力をメインバイトに入れる
        """
        return self.__inmyworld(",")
    
    # メイン位置前提 ------------------------
    def __copyto_s3(self, v):
        """
        外部のVarメインバイト値を自サブ3バイトに
        コピーする
        前提：
            値：m==x,s1==y,s2==0,s3==0,v==z
            位置：メイン位置
        結果：
            値：m==x,s1==y,s2==0,s3==z,v==z
            位置：メイン位置
        
        Parameters
        --------------
        v: Var
        
        Algorithm
        -------------
        m==x, s1==y, s2==0, s3==0, v==z
        v{
            s2++
            s3++
        }
        s2{
            v++
        }
        """
        # s2=v, s3=v, v=0
        code = (self.__outerworld(v, "[-")
                 + ">>+>+<<<"
                 + self.__outerworld(v, "]"))
        code += f">>[-<<{self.__outerworld(v, '+')}>>]<<"
        return code
    def __outerworld(self, v, code):
        return (self.__gotoG()
                 + v.__gotoM()
                 + code
                 + v.__gotoG()
                 + self.__gotoM())
    def __intheground(self, code):
        return self.__gotoG() + code + self.__gotoM()
    # 基底-メイン位置管理 -------------------
    def __inmyworld(self,code):
        return self.__gotoM()+code+self.__gotoG()
    def __gotoM(self):
        """
        go from Ground to Main
        """
        return '>' * self.m
    def __gotoG(self):
        """
        go from Main to Ground
        """
        return '<' * self.m