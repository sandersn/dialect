def sexp(s):
    if s=='()': return None
    stack = [[]]
    a = ''
    for c in s:
        if c=='(':
            if a:
                stack[-1].append((a, []))
                a = ''
            stack.append([])
        elif c==')':
            if a:
                stack[-1].append((a, []))
                a = ''
            l = stack.pop()
            stack[-1].append((l[0][0], l[1:]))
        elif c==' ':
            if a:
                stack[-1].append((a, []))
                a = ''
        else:
            a += c
    if a:
        stack[-1].append((a, []))
    return stack[0][0]
