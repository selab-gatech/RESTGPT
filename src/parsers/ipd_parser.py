import re
import yaml

class IDP_PARSER: 
    def __init__(self):
        pass
    def _logical_parse(self, logical_str):
        logical_str = logical_str.lstrip()
        logical_lhs = []
        logical_oper = ""
        logical_rhs = []

        if logical_str[0] == '(':
            parentheses_counter = 1
            for i in range(1, len(logical_str)):
                if logical_str[i] == '(':
                    parentheses_counter += 1
                elif logical_str[i] == ')':
                    parentheses_counter -= 1
                if parentheses_counter == 0:
                    logical_lhs = self._logical_parse(logical_str[1:i])
                    logical_oper = logical_str[i+2]
                    logical_rhs = self._logical_parse(logical_str[i+4:])
                    break
                elif i == len(logical_str)-1:
                    return self._logical_parse(logical_str[1:i])
        else:
            split_oper = re.split(' [&|^] ', logical_str, 1)
            logical_lhs = ['required', [split_oper[0].strip()]]
            if len(split_oper) == 2:
                logical_oper = logical_str[len(split_oper[0])+1]
                logical_rhs = self._logical_parse(split_oper[1])

        if not logical_oper:
            return logical_lhs
        elif logical_oper == '&':
            oper_str = 'allOf'
        elif logical_oper == '|':
            oper_str = 'anyOf'
        elif logical_oper == '^':
            oper_str = 'oneOf'
        
        if logical_rhs and logical_rhs[0] == '!':
            return [oper_str, logical_lhs, ['not', logical_rhs[1]]]
        else:
            return [oper_str, logical_lhs, logical_rhs]
    def _process_list(self,lst):
        for i in range(len(lst)):
            if isinstance(lst[i], list):
                self._process_list(lst[i])
                if len(lst[i])>=2 and lst[i][0] == 'required' and isinstance(lst[i][1], list):
                    if isinstance(lst[i][1][0], str) and '!' in lst[i][1][0]:
                        lst[i] = ['not', ['required', [lst[i][1][0].replace('!', '')]]]
    def _list_to_dict(self,lst):
        if isinstance(lst, list) and len(lst) == 2 and isinstance(lst[0], str) and isinstance(lst[1], list):
            return {lst[0]: self._list_to_dict(lst[1])}
        elif isinstance(lst, list) and len(lst) > 2 and isinstance(lst[0], str):
            return {lst[0]: [self._list_to_dict(item) for item in lst[1:]]}
        else:
            return lst 
    def _export_to_yaml(self, dict_obj, file_path):
        with open(file_path, 'w') as f:
            yaml.dump(dict_obj, f, default_flow_style=False)
    def parse(self, logical_str, file_path=None):
        parsed_logical = self._logical_parse(logical_str)
        self._process_list(parsed_logical)
        parsed_logical = self._list_to_dict(parsed_logical)
        if file_path:
            self._export_to_yaml(parsed_logical, file_path)
        return parsed_logical
    
class IDL_IPD_PARSER:
    def __init__(self):
        pass 
    def _logical_blocks(self, logical_str): 
        logical_str = logical_str.split("\n")
        logical_blocks = [line for line in logical_str if line.lower() != "none"]
        return logical_blocks
    def _dict_output(self, logical_blocks):
        return {"x-dependencies": logical_blocks}
    def _yaml_output(self, logical_blocks): 
        return yaml.dump(self._dict_output(logical_blocks))
    def parse(self, logical_str, r_type):
        return self._yaml_output(self._logical_blocks(logical_str)) if r_type == "yaml" else self._dict_output(self._logical_blocks(logical_str))
    