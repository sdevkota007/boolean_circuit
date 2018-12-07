input_files = ['inputs/EXTRA2.bool',
               'inputs/EXTRA1.bool',
               'inputs/test1.bool',
               'inputs/test2.bool' ,
               'inputs/test3.bool',
               'inputs/test4.bool' ,
               'inputs/test5.bool']

def neg(s):
    return '!{}'.format(s)


def write_to_file(content, filename):
    with open(filename, 'w') as f:
        f.write(content)

def read_from_file(filename):
    with open(filename) as in_file:
        content = in_file.readlines()
    return content

def main(input_file):
    lines = read_from_file(input_file)

    rows = []
    for i,line in enumerate(lines):
        if i == 0:
            variables = lines[i].split()
        else:
            rows.append(lines[i].split())
    # print(variables, rows)


    num_registers = 0
    sum_of_products = []

    for row in rows:
        if row[-1] == '1':
            expression = []
            for key, truth_value in enumerate(row):
                num_registers += 1
                if truth_value == '0':
                    expression.append(neg(variables[key]))
                else:
                    expression.append(variables[key])

                # dont execute the loop for output value
                if key == len(row)-2:
                    break
            sum_of_products.append(expression)

    # print(sum_of_products, num_registers)

    content = str(num_registers) + '\n'

    num_of_expression = len(sum_of_products)
    for i, expression in enumerate(sum_of_products):
        for variable in expression:
            if i == 0 and num_of_expression == 1:
                content = content + variable + '\t' + str(i) + '\t' + str(i + 1) + '\n'
            elif i == 0:
                content = content + variable + '\t' + str(i) + '\t' + str(i+2) + '\n'
            elif i==(num_of_expression-1):
                content = content + variable + '\t' + str(1) + '\t' + str(i+1) + '\n'
            else:
                content = content + variable + '\t' + str(i+1) + '\t' + str(i+2) + '\n'

    output_file = 'outputs/'+input_file.split('/')[1]+'.out'
    print(output_file)
    write_to_file(content, output_file)

if __name__ == '__main__':
    for input_file in input_files:
        main(input_file)