import sympy as sp

x , y = sp.symbols('x y')
 
def I(a): #단위행렬 I 정의, a는 단위행렬 차수
    imatrix = []
    for i in range(a): 
        it=[0]*a
        it[i] = 1
        imatrix.append(it)
    return imatrix

def copy_matrix(a): #del 명령어 등 사용 시 강제 전역변수 선언 후 함수 밖의 원래 행렬도 변화하는 것을 막기 위함. 행렬 a를 그대로 복사함.
    if type(a) != list: return a #a가 행렬이 아닐 때
    b = []
    for i in range(len(a)):
        it=[None]*len(a)
        for j in range(len(a[0])):
            it[j] = a[i][j]
        b.append(it)
    return b

def dot(a,b): #행렬곱 함수. axb
    if len(a[0]) != len(b): #행렬곱 정의 check
        return False
    s = [] #곱해서 나오는 결과 행렬
    for i in range(len(a)):
        it=[] #부분 행렬곱: 한 줄씩 하는 그 곱
        for j in range(len(b[0])):
            partialsum = 0
            for k in range(len(a[0])):
                if type(a[i][k]) == str or type(b[k][j]) == str: # 변수 행렬을 행렬곱할 때
                    if partialsum == 0:
                        partialsum = '((' + str(a[i][k]) + ')*(' + str(b[k][j]) + '))'
                    else:
                        partialsum = str(partialsum) + '+((' + str(a[i][k]) + ')*(' + str(b[k][j]) + '))'
                else: #type(a[i][k])와 type(b[i][k])가 모두 상수일 때.
                    if a[i][k]*b[k][j] == 0: continue
                    else:
                        if type(partialsum) == str:
                            if partialsum == '': partialsum = str(a[i][k]*b[k][j])
                            else:
                                partialsum = partialsum + '+' + str(a[i][k]*b[k][j])
                        else: #type(partialsum)이 상수
                            if partialsum == 0: partialsum = a[i][k]*b[k][j]
                            else:
                                partialsum = partialsum + a[i][k]*b[k][j]
            it.append(partialsum)
        s.append(it)
    return s

def listplist(a,b): #주의사항: 단위행렬 계산 시나 변수로 된 행렬 계산 시 반드시 걔들을 앞(a)에 넣고 상수행렬을 뒤(b)에 넣을 것!
    sum = []
    if (len(a) != len(b)) or (len(a[0]) != len(b[0])): #행렬 크기가 맞는지 check
        return False
    for i in range(len(a)):
        it=[]#고유값에서 단위행렬 I 계산 시 *주의사항: 반드시 단위행렬을 앞에 넣을 것! 만약에 둘 다 상수행렬이 아니라면 상관ㄴㄴ
        for j in range(len(a[0])):
            if type(a[i][j]) == (int or float) and type(b[i][j]) == (int or float): #상수 + 상수
                it.append(a[i][j]+b[i][j])
            else: #둘 중 하나라도 문자가 들어간 경우
                if type(a[i][j]) != (int or float) and type(b[i][j]) != (int or float): #둘 다 문자인 경우
                    it.append(sp.simplify('(' + str(a[i][j]) + ')+(' + str(b[i][j]) + ')'))
                elif type(a[i][j]) == (int or float) and type(b[i][j]) != (int or float): #우측만 문자인 경우
                    if a[i][j] == 0:
                        it.append(str(b[i][j]))
                    else: #a에 0이 아닌 상수가 있을 경우
                        it.append(sp.simplify('(' + str(a[i][j]) + ')+(' + str(b[i][j]) + ')'))
                elif type(a[i][j]) != (int or float) and type(b[i][j]) == (int or float): #좌측만 문자인 경우
                    if b[i][j] == 0:
                        it.append(str(a[i][j]))
                    else: #b에 0이 아닌 상수가 있을 경우
                        it.append(sp.simplify('(' + str(a[i][j]) + ')+(' + str(b[i][j]) + ')'))
        sum.append(it)
    return sum

def type_checker(a): #행렬 a 구성 요소 타입 체크기 : ('int or float') / 'other'
    if check_square(a) == 1: return False
    for i in range(len(a)):
        for j in range(len(a[0])):
            if type(a[i][j]) != (int or float):
                return 'other'
    return 'int or float'

def multiplyint_matrix(a,num): #행렬 a의 num배 계산
    if type(a) != list:
        if type(a) == (int or float) and type(num) == (int or float):
            return a*num
        else: #둘 중 하나라도 상수가 아닐 때
            return sp.simplify('(' + str(a) + ')*(' + str(num) + ')')
    b = copy_matrix(a) 
    for i in range(len(b)):
        for j in range(len(b[0])):
            if type(num) == (int or float):
                if type(b[i][j]) == (int or float):
                    b[i][j] *= num
                else:
                    b[i][j] = '(' + str(b[i][j]) + ')*(' + str(num) + ')'
            else:
                if b[i][j] == 0:
                    continue
                else:
                    b[i][j] = '(' + str(b[i][j]) + ')*(' + str(num) + ')'
    return b

def check_square(a): #a가 행렬인지, 그리고 정사각행렬인지 체크. 대각화 연산 전에 "if check_square():" 형태로 반드시 check할 것!
    if type(a) != list: return a #리스트 아닌 경우
    if type(a[0]) != list: return a[0] #하나의 값이 리스트에 감싸져만 있을 경우.
    length = len(a[0])
    if length != len(a): return False #정사각행렬 아닌 행렬
    for i in range(1,len(a)):
        if length != len(a[i]):
            return False #행렬 아닌 경우.
    return int(len(a)) #정사각행렬 맞으면 차수 반환

def determinent(a,checker): #변수 행렬식일 경우는 checker = 0, 상수 행렬식일 경우는 checker = 1
    if checker: #상수로만 이루어진 행렬식
        determ = 0
        if check_square(a) == 1:
            return a
        elif check_square(a) == 2:
            #print("정사각행렬",a)
            if type_checker(a) == 'other':
                return '((' + str(a[0][0]) + ')*(' + str(a[1][1]) + ')-(' + str(a[0][1]) + ')*(' + str(a[1][0]) + '))'
            else:
                return (a[0][0] * a[1][1]) - (a[0][1] * a[1][0])
        else:
            for i in range(len(a)):
                determ += a[0][i] * pow(-1,i) * determinent(eliminate_lane(a, [1,i+1]),1)
        return determ
    else: #변수가 들어간 행렬식.
        determ = ''
        if type(a) != list: return str(a) #a 타입이 리스트가 아닐 때
        elif len(a) == 2:
            return '(' + str(a[0][0]) + ')*(' + str(a[1][1]) + ')-(' + str(a[0][1]) + ')*(' + str(a[1][0]) + ')'
        else:
            for i in range(len(a)):
                # determ += a[0][i] * pow(-1,i) * determinent(eliminate_lane(a, [1,i+1]),0)
                if determ == '': #행렬식 처음 계산 시.
                    determ = "((" + str(a[0][i]) + ")*(" + str(pow(-1,i))+ ")*(" + str(determinent(eliminate_lane(a, [1,i+1]),0)) + "))"
                else:
                    determ = str(determ) + "+((" + str(a[0][i]) + ")*(" + str(pow(-1,i)) + ")*(" + str(determinent(eliminate_lane(a, [1,i+1]),0)) + "))"
    return determ #int/float 타입(상수 행렬식)이거나, str 타입(변수 행렬식)

def eliminate_lane(a,part): #소행렬 , type(part):list(행, 렬 순으로 제거할 부분 고르기), 이 함수 사용 시에는 반드시 copy_matrix 함수로 행렬 복사해서 사용할 것!
    b = copy_matrix(a) #define a as local variable as b
    part[0] -= 1
    part[1] -= 1
    if len(b) == 1:
        return b[part[0],part[1]]
    elif len(b) == 2:
        if part[0] != part[1]: return b[part[1]][part[0]]
        elif part[0] == 0: return b[1][1]
        elif part[0] == 1: return b[0][0]
    del b[part[0]]
    for i in range(len(b)):
        del b[i][part[1]]
    return b

def cofactor(a,part): #여인수(행렬식) #part에 1부터 넣을 것.
    b = copy_matrix(a)
    if type_checker(b) == 'other':
        return determinent(multiplyint_matrix(eliminate_lane(b, part),pow(-1,part[0]+part[1])),0)
    else:
        return determinent(multiplyint_matrix(eliminate_lane(b, part),pow(-1,part[0]+part[1])),1)

def transmatrix(a): #전치행렬
    if len(a) != 1 and check_square(a) == False: return False
    elif len(a) == 1: return a
    b = copy_matrix(a)
    tm = []
    for i in range(len(b)):
        it=[]
        for j in range(len(b)):
            it.append(b[j][i])
        tm.append(it)
    return tm

def inv_matrix(a,type): #역행렬. 아직 삼차 이상에서 오류 있음.
    b = copy_matrix(a)
    if type_checker(b) == 'other':
        det = sp.simplify(determinent(b, 0))
    else:
        det = determinent(b, 1)
    if det == 0: return False

    if check_square(b) == 2: #이차 정사각 행렬의 역행렬일 때.
        if type == 'fraction': #분수 타입
            if type_checker(b) == 'other':
                b = [[str(a[1][1]),'-' + str(a[0][1])],['-' + str(a[1][0]),str(a[0][0])]]
            else: #행렬 구성 요소가 전부 상수일 때.
                b = [[a[1][1],-a[0][1]],[-a[1][0],a[0][0]]]
            b = str('(1/(' + str(sp.simplify(det)) + '))*') + str(b)
        elif type == 'float': #실수 타입. 모두 상수일 때만 사용하세요!
            b = [[a[1][1],-a[0][1]],[-a[1][0],a[0][0]]]
            b = multiplyint_matrix(b, 1/det)
        return b

    im = [] #삼차 이상일 때
    if type_checker(b) == 'other':
        for i in range(len(b)): #여인수전개
            it=[]
            for j in range(len(b[0])):
                b = copy_matrix(a)
                it.append(sp.simplify(determinent(cofactor(b, [i+1,j+1]),0)))
            im.append(it)
    else:
        for i in range(len(b)): #여인수전개
            it=[]
            for j in range(len(b[0])):
                b = copy_matrix(a)
                it.append(sp.simplify(determinent(cofactor(b, [i+1,j+1]),1)))
            im.append(it)
    im = transmatrix(im)
    if type == 'fraction': #분수 타입
        if type_checker(im) == 'other':
            im = str('(1/(' + str(sp.simplify(det)) + '))*') + str(im)
    elif type == 'float': #실수 타입
        im = multiplyint_matrix(im, 1/det)
    return im

def eigenval(a): #고윳값 계산 함수
    b = copy_matrix(a)
    l = [] #고윳값 lambda
    imatrix = I(len(b))
    for i in range(len(imatrix)):
        imatrix[i][i] = str(x)
    expr = sp.sympify(determinent(listplist(imatrix,multiplyint_matrix(b, -1)),0)) #주의사항: 리스트 합 계산 시 반드시 단위행렬을 앞에 넣을 것!
    expr = sp.simplify(expr)
    l = sp.solve(expr,x) #고윳값: 리스트 타입
    return l

def eigenvector(a,l): #행렬과 고유값을 넣어주면 그에 맞는 고유벡터를 '가로로' 배열해서 반환함. 아직 이차만 가능. 삼차 이상은 sympy에서 부정방정식 푸는 법 찾아봐야 함.
    b = copy_matrix(a)
    v = []
    vectorcache = []
    
    for i in range(len(l)): #각 고윳값마다 계산
        imatrix = I(len(b))
        lmatrix = listplist(multiplyint_matrix(imatrix, l[i]),multiplyint_matrix(b, -1)) #lambda*I - A
        vectorcache = [] #각 고윳값 계산에서 벡터식 항등식 나와서 같은 벡터가 중복으로 들어가는 것 막기 위함.
        for j in range(len(lmatrix)): #고윳값 적용한 행렬과 벡터를 곱했을 때 각각의 벡터식 계산.
            expr = sp.sympify('(' + str(lmatrix[j][0]) + ')+(' + str(lmatrix[j][1]) + ')*(y)') #x = 1로 가정한 후 그에 따른 y값 구하기
            expr = sp.solve(expr,y) #type(expr) = list
            for k in range(len(expr)):
                if not([1,expr[k]] in vectorcache):
                    vectorcache.append([1,expr[k]])
                    v.append([1,expr[k]]) #x = 1로 가정했으므로 1이다.
    return v

def diagonalize(a): #대각화 함수. 위에 있는 '모든' 함수가 필요합니다.
    p = []
    d = []
    ip = []
    if check_square(a) == 1:
        return 'It isn\'t need to diag' #대각화 필요X
    elif check_square(a) == False:
        return False #대각화 불능
    elif check_square(a) >= 3:
        return 'developing..' #고유벡터에서 부정방정식 때문에 문제 생김. 그래서 막아 둠.
    l = eigenval(a)
    v = eigenvector(a, l)
    if len(v) != len(a): return False #행렬 차수 = 고유벡터 수이므로!

    p = I(len(l))
    for i in range(len(v)):
        for j in range(len(v[0])):
            p[i][j] = sp.simplify(v[j][i])

    d = I(len(l))
    for i in range(len(l)):
        d[i][i] = l[i]

    ip = inv_matrix(p, 'float')

    return [p,d,ip]

def convert(expr):
    expression = expr.split("=")
    constant = expression[1] #상수항
    expression[0] = expression[0].split("x")
    a = float(expression[0][0]) #x^2항
    b = float(expression[0][1][2:]) #xy항
    c = float(expression[0][2].split("y")[1].split("+")[1]) #y^2항
    diaged_matrix = diagonalize([[a,b/2],[b/2,c]])
    tanθ = max(((c-a) + (((c-a)**2)+(4*(b**2)))**0.5)/(2*b),((c-a) - (((c-a)**2)+(4*(b**2)))**0.5)/(2*b))
    return [diaged_matrix[1][0][0],diaged_matrix[1][1][1]],constant,tanθ #[[x^2 계수, y^2 계수],상수항,탄젠트 회전각]

info = convert(input("수식을 'ax^2+bxy+cy^2=상수' 형식으로 입력해 주세요. 일차항은 아직 개발 안 됐습니다. : ")) #수식을 넣으면 좌표축을 변환한 행렬의 [[x^2 계수, y^2 계수],상수항,탄젠트 회전각]가 리스트 형태로 반환.
print('회전각 tanθ =',info[2],'입니다.')

if info[0][0]%1 == 0 and info[0][1]%1 == 0:
    print('변환된 식은 ',int(info[0][0]),'x^2+',int(info[0][1]),'y^2=',info[1],'입니다.',sep='')
elif info[0][0]%1 != 0 and info[0][1]%1 == 0:
    print('변환된 식은 ',info[0][0],'x^2+',int(info[0][1]),'y^2=',info[1],'입니다.',sep='')
elif info[0][0]%1 == 0 and info[0][1]%1 != 0:
    print('변환된 식은 ',int(info[0][0]),'x^2+',info[0][1],'y^2=',info[1],'입니다.',sep='')
