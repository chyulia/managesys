
import os
AllElements = ['CRU']

if __name__ == '__main__':
    cur_path = os.path.abspath('.')
    cur_par_path = os.path.dirname(cur_path)
    print(cur_par_path)
    sh_path = os.path.join(cur_par_path, 'scrapy_elements', 'scrapy')
    sh_cmd = os.path.join(sh_path, 'scrapy_elements.sh')
    for ele_type in AllElements:
        cmd_params= " ".join([ sh_cmd, sh_path, ele_type])
        print(cmd_params)
        os.system(cmd_params)