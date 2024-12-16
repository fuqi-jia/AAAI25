import sys
import re
import os
import shutil

file_name = sys.argv[1]
# out_dir = sys.argv[2]
replace_invalid_variable_name = dict()
variable_types = dict()

def is_legal(s):
    return s == "_" or s == "~" or s == "|" or s.isalnum()

def get_variable_name(name):
    global replace_invalid_variable_name
    if '|' in name and name not in replace_invalid_variable_name:
        new_name = f"VAR{len(replace_invalid_variable_name)}_"
        replace_invalid_variable_name[name] = new_name
        return new_name
    if name not in replace_invalid_variable_name:
        return name
    else:
        return replace_invalid_variable_name[name]

def get_formula(suffix, t, s, variables):
    # 遍历变量列表，将s和t中的每个变量都加上后缀
    new_s = s
    new_t = t
    new_t = get_term(suffix, new_t, variables)
    if suffix != "":
        for var in variables:
            for i in range(len(new_s)):
                index = 0
                while index < len(new_s[i]):
                    # print(s[i][index - 10:index + 10])
                    index = new_s[i].find(var, index)
                    # print(s[i][:index] + "^" + s[i][index:])
                    if index == -1: break
                    start, end = index, index + len(var)
                    index = end
                    assert new_s[i][start:end] == var
                    if (not is_legal(new_s[i][start-1]) if start-1 < len(new_s[i]) and start - 1 >= 0 else True) and (not is_legal(new_s[i][end]) if end < len(new_s[i]) else True):
                        if '|' in var:
                            # print(new_s[i][start:end-1], var)
                            # new_s[i] = new_s[i][:end-1] + suffix + new_s[i][end-1:]
                            # print(var)
                            # print('i', new_s[i])
                            new_s[i] = new_s[i][:start] + get_variable_name(var) + new_s[i][end:]
                            # print('o', new_s[i])
                        else:
                            new_s[i] = new_s[i][:end] + suffix + new_s[i][end:]

    # # 将“t0“=t、s中的各个约束使用and约束并起来
    # formula = f'(= {new_var} {new_t})'
    if new_s:
        formula = f'(and {" ".join(new_s)})'

    return formula

def get_term(suffix, t, variables):
    new_t = t
    if suffix != "":
        for var in variables:
            index = 0
            while index < len(new_t):
                index = new_t.find(var, index)
                if index == -1: break
                start, end = index, index + len(var)
                index = end
                assert new_t[start:end] == var
                if (not is_legal(new_t[start-1]) if start-1 < len(new_t) and start - 1 >= 0 else True) and (not is_legal(new_t[end]) if end < len(new_t) else True):
                    if '|' in var:
                        # print(new_t[start:end-1], var)
                        # new_t = new_t[:end-1] + suffix + new_t[end-1:]
                        new_t = new_t[:start] + get_variable_name(var) + new_t[end:]
                    else:
                        new_t = new_t[:end] + suffix + new_t[end:]
    return new_t

def add_forall(var_name, formula, suffix="_tmp"):
    global variable_types
    # print("forall", var_name, variable_types[var_name])
    new_var_name = var_name + suffix if '|' not in var_name else get_variable_name(var_name)
    type = variable_types[var_name] if var_name in variable_types else "Real"
    formula = f"(forall (({new_var_name} {type})) {formula})"
    return formula

def add_exists(var_name, formula, suffix="_tmp"):
    global variable_types
    new_var_name = var_name + suffix if '|' not in var_name else get_variable_name(var_name) 
    type = variable_types[var_name] if var_name in variable_types else "Real"
    formula = f"(exists (({new_var_name} {type})) {formula})"
    return formula

def replace_define_fun(lines):
    replace_map = {}
    # (define-fun hypothesis () Bool (and (= v6 0) (< v7 0)))
    # make dict[hypothesis] = (and (= v6 0) (< v7 0))
    res = []
    line_tmp = ""
    flag = False
    current_name = ""
    for line in lines:
        if line.startswith(';'):
            pass
        elif line.startswith("(define-fun"):
            if flag:
                replace_map[current_name] = line_tmp[:-1]
            flag = True
            line_tmp = ""
            line_tmp += line.split("(define-fun ")[1].split(" () ")[1]
            line_tmp = line_tmp.replace("Bool ", "")
            line_tmp = line_tmp.replace("Real ", "")
            line_tmp = line_tmp.replace("Int ", "")
            line_tmp = line_tmp.replace("Bool", "")
            line_tmp = line_tmp.replace("Real", "")
            line_tmp = line_tmp.replace("Int", "")
            line_tmp.strip()
            current_name = line.split("(define-fun ")[1].split(" ")[0]
        elif flag and (line.startswith("(minimize") or line.startswith("(assert") or line.startswith("(declare")):
            replace_map[current_name] = line_tmp[:-1]
            line_tmp = ""
            current_name = ""
            flag = False
        elif flag:
            line_tmp += line

    # print(replace_map)

    flag = False
    for line in lines:
        if line.startswith("(define-fun"):
            flag = True
            continue
        elif flag and (line.startswith("(minimize") or line.startswith("(assert") or line.startswith("(declare") or line.startswith("(define-fun")):
            flag = False
        elif flag:
            continue
        
        if line.startswith("(assert"):
            for key in replace_map.keys():
                line = line.replace(key, replace_map[key])

        res.append(line)

    return res


def omt_convert_to_quantified_smt(formula):
    # 分割公式为多行
    init_lines = formula.split('\n')
    lines = []
    flag = False
    line_tmp = ""

    init_lines = replace_define_fun(init_lines)

    for line in init_lines:
        if not flag and not line.startswith("(assert"):
            lines.append(line)
        if line.startswith("(minimize"):
            lines.append(line_tmp)
            lines.append(line)
            flag = False
            line_tmp = ""
        elif line.startswith("(declare"):
            if flag:
                lines.append(line_tmp)
                line_tmp = ""
                lines.append(line)
                flag = False
        elif line.startswith("(assert"):
            if flag:
                lines.append(line_tmp)
                line_tmp = ""
            flag = True
            line_tmp += line
        elif flag:
            line_tmp += line

    # 找到所有的assert语句和minimize语句
    declare_statements = [line for line in lines if line.startswith('(declare')]
    assert_statements = [line for line in lines if line.startswith('(assert')]
    minimize_statement = next(line for line in lines if line.startswith('(minimize'))

    # 提取优化目标
    # v = [line.split(" ")[1] for line in declare_statements]
    v = []
    global variable_types
    for line in declare_statements:
        var_name = ""
        var_type = ""
        if '|' in line:
            var_name = '|'+line.split("|")[1]+'|'
            if "declare-const" in line:
                var_type = line.split("|")[2].split(" ")[1][:-1]
            else:
                var_type = line.split("|")[2].split(" ")[2][:-1]
        else:
            var_name = line.split(" ")[1]
            if "declare-const" in line:
                var_type = line.split(" ")[2][:-1]
            else:
                var_type = line.split(" ")[3][:-1]
        v.append(var_name)
        
        variable_types[var_name] = var_type

    # print(variable_types)
    
    s = [line.replace("(assert ", "")[:-1] for line in assert_statements]
    t = re.search(r'\(minimize (.+)\)', minimize_statement).group(1)
    formula = {
        "fixity": omt_convert_to_quantified_smt_fixity(v, s, t),
        "asymptote": omt_convert_to_quantified_smt_asymptote(v, s, t),
        "infty": omt_convert_to_quantified_smt_infty(v, s, t)
    }
    
    # 形成SMT公式
    new_lines = ["(set-logic NRA)"] + declare_statements + [
        '(declare-fun OPT_VALUE_ () Real)',
        '(declare-fun FIXITY_ () Bool)',
        '(declare-fun ASYMPTOTE_ () Bool)',
        '(declare-fun UNBOUNDNESS_ () Bool)'
    ]
    # new_lines = [line.replace("QF_", "") if line.startswith('(set-logic') else line for line in new_lines]
    
    # 将新的函数公式添加到新的公式中
    new_lines.append(f'(assert (=> FIXITY_ {formula["fixity"]}))')
    new_lines.append(f'(assert (=> ASYMPTOTE_ {formula["asymptote"]}))')
    new_lines.append(f'(assert (=> UNBOUNDNESS_ {formula["infty"]}))')
    # new_lines.append(f'(assert (or (and (not FINITY_) INFTY_) (and (not INFTY_) FINITY_)))')
    new_lines.append(f'(assert (or (and FIXITY_ (not ASYMPTOTE_) (not UNBOUNDNESS_)) (and (not FIXITY_) ASYMPTOTE_ (not UNBOUNDNESS_)) (and (not FIXITY_) (not ASYMPTOTE_) UNBOUNDNESS_)))')
    # new_lines.append(f'(assert (or FIXITY_ ASYMPTOTE_ UNBOUNDNESS_))')
    new_lines.append('(check-sat)')
    new_lines.append(f'(get-value (OPT_VALUE_))')
    new_lines.append(f'(get-value (FIXITY_))')
    new_lines.append(f'(get-value (ASYMPTOTE_))')
    new_lines.append(f'(get-value (UNBOUNDNESS_))')
    new_lines.append('(exit)')

    return '\n'.join(new_lines)

def omt_convert_to_quantified_smt_infimum(v, s, t):
    opt_val = "OPT_VALUE_"
    func_formula = get_formula("", t, s, v)
    func_formula_tmp = get_formula("_tmp", t, s, v)
    forall_formula = f"(=> {func_formula} (<= {opt_val} {t}))"

    for i in range(len(v)-1, -1, -1):
        forall_formula = add_forall(v[i], forall_formula, "")

    lower_bound_formula = f"(=> {func_formula_tmp} (<= LOWER_BOUND_ {get_term('_tmp', t, v)}))"
    for i in range(len(v)-1, -1, -1):
        lower_bound_formula = add_forall(v[i], lower_bound_formula, "_tmp")
    largest_formula = f"(forall ((LOWER_BOUND_ Real)) (=> {lower_bound_formula} (<= LOWER_BOUND_ {opt_val})))"

    formula = f"(and {largest_formula} {forall_formula})"

    return formula

def omt_convert_to_quantified_smt_fixity(v, s, t):
    opt_val = "OPT_VALUE_"
    func_formula = get_formula("", t, s, v)
    func_formula_tmp = get_formula("_tmp", t, s, v)
    forall_formula = f"(=> {func_formula_tmp} (<= {opt_val} {get_term('_tmp', t, v)}))"

    for i in range(len(v)-1, -1, -1):
        forall_formula = add_forall(v[i], forall_formula, "_tmp")

    formula = f"(and {func_formula} {forall_formula} (= {get_term('', t, v)} {opt_val}))"

    return formula

def omt_convert_to_quantified_smt_asymptote(v, s, t):
    opt_val = "OPT_VALUE_"
    func_formula_tmp = get_formula("_tmp", t, s, v)
    forall_formula = f"(=> {func_formula_tmp} (< {opt_val} {get_term('_tmp', t, v)}))"

    # eps_formula = f"(forall ((EPSILON_ Real)) (=> (> EPSILON_ 0) (< {get_term('_tmp', t, v)} (+ {opt_val} EPSILON_))))"
    eps_formula = f"(=> (> EPSILON_ 0) (and {func_formula_tmp} (< {get_term('_tmp', t, v)} (+ {opt_val} EPSILON_))))"
    # eps_formula = f"(and {func_formula_tmp} {eps_formula})"
    # forall_formula = f"(=> {func_formula_tmp} (and (< {opt_val} {get_term('_tmp', t, v)}) {eps_formula}))"
    # forall_formula = f"(and {forall_formula} {eps_formula})"
    # (forall ((EPSILON_ Real)) )

    for i in range(len(v)-1, -1, -1):
        forall_formula = add_forall(v[i], forall_formula, "_tmp")

    for i in range(len(v)-1, -1, -1):
        eps_formula = add_exists(v[i], eps_formula, "_tmp")
    eps_formula = f"(forall ((EPSILON_ Real)) {eps_formula})"

    formula = f"(and {forall_formula} {eps_formula})"

    return formula

def omt_convert_to_quantified_smt_infty(v, s, t):
    # 获取新公式
    func_formula = get_formula("", t, s, v)
    # print(func_formula)

    exists_formula = f"(and {func_formula} (<= {get_term('_tmp', t, v)} Minus_Infty_))"
    for i in range(len(v)-1, -1, -1):
        exists_formula = add_exists(v[i], exists_formula, "_tmp")
    exists_formula = f"(forall ((Minus_Infty_ Real)) {exists_formula})"

    return exists_formula

def verif_convert_to_quantified_smt(formula, var, opt):
    # 分割公式为多行
    init_lines = formula.split('\n')
    lines = []
    flag = False
    line_tmp = ""

    for line in init_lines:
        if not flag and not line.startswith("(assert"):
            lines.append(line)
        if line.startswith("(minimize"):
            lines.append(line_tmp)
            lines.append(line)
            flag = False
            line_tmp = ""
        elif line.startswith("(declare"):
            if flag:
                lines.append(line_tmp)
                line_tmp = ""
                lines.append(line)
                flag = False
        elif line.startswith("(assert"):
            if flag:
                lines.append(line_tmp)
                line_tmp = ""
            flag = True
            line_tmp += line
        elif flag:
            line_tmp += line

    # 找到所有的assert语句和minimize语句
    declare_statements = [line for line in lines if line.startswith('(declare')]
    assert_statements = [line for line in lines if line.startswith('(assert')]
    minimize_statement = next(line for line in lines if line.startswith('(minimize'))

    # 提取优化目标
    v = [line.split(" ")[1] for line in declare_statements]
    s = [line.replace("(assert ", "")[:-1] for line in assert_statements]
    t = var
    
    if "infty" in opt['type']:
        # 获取新公式
        func_formula = get_formula("", t, s, v)
        # print(s)
        # print(func_formula)
        exists_formula = f"(and {func_formula} (<= {t} Minus_Infty_))"
        # print(exists_formula)
        for i in range(len(v)-1, -1, -1):
            exists_formula = add_exists(v[i], exists_formula, "")
        exists_formula = f"(assert (forall ((Minus_Infty_ Real)) {exists_formula}))"

        # 形成SMT公式
        new_lines = ["(set-logic NRA)"] + declare_statements
        # for i in range(len(declare_statements)):
        #     new_lines.append(declare_statements[i].replace(v[i], v[i]+"_tmp"))
        new_lines = [line.replace("QF_", "") if line.startswith('(set-logic') else line for line in new_lines]
        
        # 将新的函数公式添加到新的公式中
        new_lines.append(exists_formula)
        new_lines.append('(check-sat)')
        new_lines.append('(exit)')

        return '\n'.join(new_lines)
    else:
        # 获取新公式
        func_formula = get_formula("", t, s, v)
        func_formula_tmp = get_formula("_tmp", t, s, v)
        forall_formula = None
        largest_formula = None
        value = opt['value']
        if "epsilon" in opt['type']:
            forall_formula = f"(=> {func_formula} (< {value} {t}))"
        else:
            forall_formula = f"(=> {func_formula} (<= {value} {t}))"

        for i in range(len(v)-1, -1, -1):
            forall_formula = add_forall(v[i], forall_formula, "")
        
        lower_bound_formula = f"(=> {func_formula_tmp} (<= LOWER_BOUND_ {get_term('_tmp', t, v)}))"
        for i in range(len(v)-1, -1, -1):
            lower_bound_formula = add_forall(v[i], lower_bound_formula, "_tmp")
        largest_formula = f"(forall ((LOWER_BOUND_ Real)) (=> {lower_bound_formula} (<= LOWER_BOUND_ {value})))"


        forall_formula = f"(assert (and {largest_formula} {forall_formula}))"

        # 形成SMT公式
        new_lines = ["(set-logic NRA)"] + declare_statements
        # for i in range(len(declare_statements)):
        #     new_lines.append(declare_statements[i].replace(v[i], v[i]+"_tmp"))
        new_lines = [line.replace("QF_", "") if line.startswith('(set-logic') else line for line in new_lines]
        
        # 将新的函数公式添加到新的公式中
        if "real_algebraic_number" in opt['type']:
            new_lines.append(opt["constraint"])
        new_lines.append(forall_formula)
        new_lines.append('(check-sat)')
        new_lines.append('(exit)')

        return '\n'.join(new_lines)

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    paths = "/".join(file_path.split("/")[:-1])
    if not os.path.exists(paths):
        os.makedirs(paths)

    with open(file_path, 'w') as file:
        file.write(content)

if __name__ == '__main__':
    input_file_path = file_name 

    original_formula = read_file(input_file_path)
    new_formula = omt_convert_to_quantified_smt(original_formula)
    write_file(input_file_path, new_formula)