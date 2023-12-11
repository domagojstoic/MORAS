def _parse_macros(self):
    self._init_macros()
    self._iter_lines(self._parse_macro)

def _parse_macro(self,line,p,o):
    if len(line)<=0:
        return ""
    if (line[0]=="$"):
        vars=[]
        macro=line[1:].split("(")
        print(macro)
        if len(macro)==1 and macro[0]!="END":
            self._flag = False
            self._line = o
            self._errm = "Invalid macro"
            return ""
        elif macro[0]!="END":
            temp=macro[1]
            macro=macro[0]
            if "," in temp:
                temp=temp.split(",")
                for i in range(len(temp)-1):
                    vars.append(temp[i])
                temp=temp[-1]
            if ")" in temp:
                temp=temp.split(")")
                vars.append(temp[0])
                temp=temp[1]
            if len(temp)!=0:
                self._flag = False
                self._line = o
                self._errm = "Invalid macro"
                return ""
        else:
            macro=macro[0] 
        if [2,2,3,1,0][(["MV","SWP","SUM","WHILE","END"].index(macro))]!=len(vars):
            self._flag = False
            self._line = o
            self._errm = "Wrong number of arguments"
            return ""
        if macro=="WHILE":
            self._loop_number+=1
        if macro in self._macros:
            expansion=self._macros[macro]
            for i in range(len(vars)):
                expansion=expansion.replace(["a","b","c"][i],vars[i])
            expansion=expansion.replace("loop_number",str(self._loop_number))
            expansion=expansion.split(":")
            for lines in expansion:
                self._lines.insert(int(o)+1,(lines,p,o))
                o+=1
                for i in range(p,len(self._lines)):
                    (a,b,c)=self._lines[i]
                    self._lines[i]=(a,b,c+1)
            if macro=="END":
                self._loop_number-=1
            return ""
        else:
            self._flag = False
            self._line = o
            self._errm = "Macro doesnt exist"
            return ""

    else:
        return line

def _init_macros(self):
    self._macros={
        "MV":"@a:D=M;:@a:M=D;",
        "SWP":"@a:D=M;:@b:M=M+D;:D=M-D;:M=M-D;:@a:M=D;",
        "SUM":"@a:D=M;:@b:D=D+M;:@c:M=D;",
        "WHILE":"(LOOP_loop_number_START):@a:D=M;:@LOOP_loop_number_END:D;JNE",
        "END":"@LOOP_loop_number_START:0;JMP:(LOOP_loop_number_END)"
        }
