import os,random,sys,string
from lark import Lark, Transformer, Token

args = sys.argv

infile = args[1]

includes = ["\"defaults.hpp\""]

class ASTTransformer(Transformer):
	def var(self,body):
		return {
			"type": "var",
			"details": {
				"vtype": body[0],
				"type": body[1],
				"name": body[2],
				"value": body[3]
			}
		}

	def auto_var(self,body):
		return {
			"type": "auto_var",
			"details": {
				"vtype": body[0],
				"name": body[1],
				"value": body[2]
			}
		}

	def string_type(self,body):
		if not "<string>" in includes:
			includes.append("<string>")
			
		return "std::string"

	def int_type(self,body):
		return "int"

	def void_type(self,body):
		return "void"

	def string(self,body):
		return body[0]

	def number(self,body):
		return body[0]

	def access_var(self,body):
		return {
			"type": "access_var",
			"details": {
				"name": body[0]
			}
		}

	def start(self,body):
		return body

	def scope(self,body):
		return body

	def func(self,body):
		return {
			"type": "func",
			"details": {
				"template": body[0],
				"type": body[1],
				"name": body[2],
				"params": body[3],
				"body": body[4]
			}
		}

	def var_keyword(self,body):
		return "var"

	def mut_keyword(self,body):
		return "mut"

	def add(self,body):
		return {
			"type": "add",
			"details": {
				"left": body[0],
				"right": body[1]
			}
		}

	def sub(self,body):
		return {
			"type": "sub",
			"details": {
				"left": body[0],
				"right": body[1]
			}
		}

	def mul(self,body):
		return {
			"type": "mul",
			"details": {
				"left": body[0],
				"right": body[1]
			}
		}

	def div(self,body):
		return {
			"type": "div",
			"details": {
				"left": body[0],
				"right": body[1]
			}
		}

	def mod(self,body):
		return {
			"type": "mod",
			"details": {
				"left": body[0],
				"right": body[1]
			}
		}

	def call_func_val(self,body):
		return {
			"type": "call_func",
			"details": {
				"name": body[0],
				"args": body[1],
				"val": True
			}
		}

	def call_func_no_args_val(self, body):
		return {
			"type": "call_func",
			"details": {
				"name": body[0],
				"args": [],
				"val": True
			}
		}

	def call_func(self,body):
		return {
			"type": "call_func",
			"details": {
				"name": body[0],
				"args": body[1],
				"val": False
			}
		}

	def call_func_no_args(self, body):
		return {
			"type": "call_func",
			"details": {
				"name": body[0],
				"args": [],
				"val": False
			}
		}

	def return_statement(self,body):
		return {
			"type": "return",
			"details": {
				"value": body[0]
			}
		}

	def params(self,body):
		return body

	def param(self,body):
		return {
			"template": False,
			"type": body[0],
			"name": body[1]
		}

	def valerdic_param(self,body):
		return {
			"template": True,
			"type": body[0],
			"name": body[1]
		}

	def args(self,body):
		return body

	def arg(self,body):
		return {
			"value": body[0]
		}

	def assign(self,body):
		return {
			"type": "assign",
			"details": {
				"name": body[0],
				"value": body[1]
			}
		}

	def bool_type(self,body):
		return "bool"

	def true(self,body):
		return "true"

	def false(self,body):
		return "false"

	def num_type(self,body):
		return "float"

	def char_type(self,body):
		return "char"

	def array(self,body):
		return {
			"type": "array",
			"details": {
				"items": body
			}
		}

	def item(self,body):
		return body

	def array_type(self,body):
		return f"Array<{body[0]}>"

	def array_access(self,body):
		return {
			"type": "array_access",
			"details": {
				"name": body[0],
				"index": body[1]
			}
		}

	def for_loop(self,body):
		return {
			"type": "for",
			"details": {
				"type": body[0],
				"name": body[1],
				"from": body[2],
				"to": body[3],
				"body": body[4]
			}
		}

	def method(self,body):
		return {
			"type": "method",
			"details": {
				"parent": body[0],
				"name": body[1],
				"args": body[2],
				"val": False
			}
		}

	def method_no_args(self,body):
		return {
			"type": "method",
			"details": {
				"parent": body[0],
				"name": body[1],
				"args": [],
				"val": False
			}
		}

	def method_val(self,body):
		return {
			"type": "method",
			"details": {
				"parent": body[0],
				"name": body[1],
				"args": body[2],
				"val": True
			}
		}

	def method_no_args_val(self,body):
		return {
			"type": "method",
			"details": {
				"parent": body[0],
				"name": body[1],
				"args": [],
				"val": True
			}
		}

	def lambda_func(self,body):
		return {
			"type": "lambda",
			"details": {
				"type": body[0],
				"params": body[1],
				"body": body[2]
			}
		}

	def prop(self,body):
		return {
			"type": "prop",
			"details": {
				"parent": body[0],
				"name": body[1]
			}
		}

	def length_access(self,body):
		return {
			"type": "array_length",
			"details": {
				"name": body[0]
			}
		}

	def no_dec_var(self,body):
		return {
			"type": "no_dec_var",
			"details": {
				"vtype": body[0],
				"type": body[1],
				"name": body[2]
			}
		}

	def lambda_type(self,body):
		if not "<functional>" in includes:
			includes.append("<functional>")

		lam = f"std::function<{body[1]}("

		for i,t in enumerate(body[0]):
			lam += t
			if i != len(body[0]) - 1: lam += ","
		
		lam += ")>"
		
		return lam

	def lambda_params(self,body):
		return body

	def custom_type(self,body):
		return body[0].value

	def template(self,body):
		return body

parser = Lark("""
	 ?start: (func)* -> start
	
	 ?expr: var_type type VARNAME "=" val -> var
		| var_type VARNAME ":=" val       -> auto_var
		| var_type type VARNAME           -> no_dec_var
		| "return" val                    -> return_statement
		| assign_var
		| method_call
		| VARNAME args     -> call_func
		| VARNAME "(" ")"  -> call_func_no_args
		| for_loop

	 ?method_call: (VARNAME | prop) "." VARNAME args -> method
		| (VARNAME | prop) "." VARNAME "(" ")"       -> method_no_args
			  
	 ?type: "string"   -> string_type
	 	| "int"        -> int_type
		| "bool"       -> bool_type
		| "num"        -> num_type
		| "char"       -> char_type
		| type "[" "]" -> array_type
		| "lambda" lambda_params ">" return_type -> lambda_type
		| "~" VARNAME -> custom_type

	 ?lambda_params: "(" type ("," type) ")" -> lambda_params
		| lambda_params? -> lambda_params

	 ?return_type: type
		| "void" -> void_type

	 ?var_type: "var" -> var_keyword
		| "mut"       -> mut_keyword

	 ?assign_var: VARNAME "=" val -> assign

	 ?val: NUMBER     -> number
		| STRING      -> string
		| VARNAME     -> access_var
		| val "+" val -> add
		| val "-" val -> sub
		| val "*" val -> mul
		| val "/" val -> div
		| val "%" val -> mod
		| "true"      -> true
		| "false"     -> false
		| array
		| VARNAME "[" STRING "]"               -> dict_access
		| VARNAME "[" val "]"                  -> array_access
		| "#" VARNAME                          -> length_access
		| VARNAME args                         -> call_func_val
		| VARNAME "(" ")"                      -> call_func_no_args_val
		| (VARNAME | prop) "." VARNAME args    -> method_val
		| (VARNAME | prop) "." VARNAME "(" ")" -> method_no_args_val
		| lambda
		| prop

	 ?array: "[" item ("," item)* "]" -> array
	 ?item: val                       -> item

	 ?prop: VARNAME "." VARNAME -> prop
		| prop "." VARNAME      -> prop

	 ?lambda: return_type params ">" (val | scope) -> lambda_func

	 ?for_loop: "for" var_type VARNAME "from" val "to" val scope -> for_loop
			  
	 ?scope: "{" expr* "}" -> scope
			  
	 ?func: "func" template return_type VARNAME params ("=" val | scope) -> func
	 ?template: "<" VARNAME ">" -> template
		| template? -> template
			  
	 ?params: "(" param ("," param)* ")" -> params
		| "(" params? ")"                -> params
			  
	 ?param: type VARNAME      -> param
		| "..." type VARNAME   -> valerdic_param

	 ?args: "(" arg ("," arg)* ")" -> args
			  
	 ?arg: val -> arg
			  
	 COMMENT: "//" /[^\\n]*/
	 VARNAME: /[a-zA-Z_][a-zA-Z0-9_]*/

	 %import common.ESCAPED_STRING -> STRING
	 %import common.SIGNED_NUMBER  -> NUMBER
	 %import common.WS_INLINE

	 %ignore WS_INLINE
	 %ignore "\\n"
	 %ignore COMMENT
""",parser="lalr")

code = ""

with open(infile,"r") as f:
	code = f.read()

tree = parser.parse(code)
ast = ASTTransformer().transform(tree)
funcname = "".join(random.choices(string.ascii_letters,k=10))

def translate(ex):
	if type(ex) == Token:
		if ex.type == "STRING": return ex.value
		elif ex.type == "NUMBER": return ex.value
		elif ex.type == "VARNAME": return ex.value
			
	elif type(ex) == str:
		return ex
	
	elif ex["type"] == "func":
		data = ex["details"]

		func = ""
		T = ""

		if len(data["template"]) != 0:
			if data["name"] == "main":
				raise Exception("Cannot template main function.")
				
			T += "template<"

			for i,template in enumerate(data["template"]):
				T += f"typename {translate(template)}"
				if i != len(data["template"]) - 1: T += ","

		if data["name"] == "main":
			if data["type"] != "void":
				raise Exception("Main function must be return type \"void\"")
				
			func = "void main_%s(" % funcname

		else:
			func += f"{data['type']} {data['name']}("

		convert = False
		vtype = ""
		vname = ""
		for i,param in enumerate(data["params"]):
			if param["template"]:
				if len(data["template"]) != 0:
					T += f",typename... {funcname[:5]}"
				else:
					T += f"template<typename... {funcname[:5]}> "

				vname = param["name"]
				vtype = param["type"]
				func += f"{funcname[:5]}... {funcname[:7]}"
				convert = True
				
			else:
				func += f"{param['type']} {param['name']}"
			
			if i != len(data["params"]) - 1: func += ","
		
		func += "){"

		if convert == True:
			func += f"Array<{vtype}> {vname}({funcname[:7]}...);"
		
		if type(data["body"]) == dict or type(data["body"]) == Token:
			func += f"return {translate(data['body'])};"

		else:
			for b in data["body"]:
				func += translate(b)

		if len(data["template"]) != 0:
			T += ">"
		func += "}"
		
		return T + func
		
	elif ex["type"] == "var":
		data = ex["details"]

		if data["vtype"] == "var":
			if data["type"][:5] == "Array":
				return f"const {data['type']} {data['name']}{translate(data['value'])};"
			else:
				return f"const {data['type']} {data['name']}={translate(data['value'])};"

		elif data["vtype"] == "mut":
			if data["type"][:5] == "Array":
				return f"{data['type']} {data['name']}{translate(data['value'])};"
			else:
				return f"{data['type']} {data['name']}={translate(data['value'])};"

	elif ex["type"] == "auto_var":
		data = ex["details"]

		if data["vtype"] == "var":
			return f"const auto {data['name']}={translate(data['value'])};"

		elif data["vtype"] == "mut":
			return f"auto {data['name']}={translate(data['value'])};"

	elif ex["type"] == "access_var":
		return ex["details"]["name"]

	elif ex["type"] == "add":
		data = ex["details"]

		return f"{translate(data['left'])}+{translate(data['right'])}"

	elif ex["type"] == "sub":
		data = ex["details"]

		return f"{translate(data['left'])}-{translate(data['right'])}"

	elif ex["type"] == "mul":
		data = ex["details"]

		return f"{translate(data['left'])}*{translate(data['right'])}"

	elif ex["type"] == "div":
		data = ex["details"]

		return f"{translate(data['left'])}/{translate(data['right'])}"

	elif ex["type"] == "mod":
		data = ex["details"]

		return f"{translate(data['left'])}%{translate(data['right'])}"

	elif ex["type"] == "call_func":
		data = ex["details"]
		func = f"{data['name']}("

		for i,arg in enumerate(data["args"]):
			func += translate(arg["value"])
			if i != len(data["args"]) - 1: func += ","

		func += ")"

		if data["val"] == False:
			func += ";"
		
		return func

	elif ex["type"] == "return":
		data = ex["details"]

		return f"return {translate(data['value'])};"

	elif ex["type"] == "assign":
		data = ex["details"]

		return f"{data['name']}={translate(data['value'])};"

	elif ex["type"] == "array":
		data = ex["details"]

		arr = "("

		for i,it in enumerate(data["items"]):
			for v in it:
				arr += translate(v)
				
			if i != len(data["items"]) - 1: arr += ","

		arr += ")"
		
		return arr

	elif ex["type"] == "array_access":
		data = ex["details"]

		return f"{data['name']}.get({translate(data['index'])})"

	elif ex["type"] == "for":
		data = ex["details"]

		forc = ""
		if data['type'] == "mut":
			forc = f"for(int {translate(data['name'])}={translate(data['from'])};{translate(data['name'])}<{translate(data['to'])};{translate(data['name'])}++)"
		
		else:
			forc = f"for(const int {translate(data['name'])}={translate(data['from'])};{translate(data['name'])}<{translate(data['to'])};{translate(data['name'])}++)"
		
		forc += "{"

		for b in data['body']:
			forc += translate(b)

		forc += "}"

		return forc

	elif ex["type"] == "method":
		data = ex["details"]

		met = f"{translate(data['parent'])}.{data['name']}("

		for i,arg in enumerate(data["args"]):
			met += translate(arg["value"])
			if i != len(data["args"]) - 1: met += ","

		met += ")"

		if data["val"] == False:
			met += ";"
		
		return met

	elif ex["type"] == "lambda":
		data = ex["details"]

		func = "[=]("

		for i,param in enumerate(data["params"]):
			func += f"{param['type']} {param['name']}"
			if i != len(data["params"]) - 1: func += ","

		func += f")->{data['type']}"
		func += "{"

		if type(data["body"]) == dict or type(data["body"]) == Token:
			func += f"return {translate(data['body'])};"

		else:
			for b in data["body"]:
				func += translate(b)

		func += "}"

		return func

	elif ex["type"] == "prop":
		return f"{translate(ex['details']['parent'])}.{ex['details']['name']}"

	elif ex["type"] == "array_length":
		return f"{translate(ex['details']['name'])}.length()"

	elif ex["type"] == "no_dec_var":
		data = ex["details"]

		if data["vtype"] == "var":
			return f"const {ex['details']['type']} {translate(ex['details']['name'])};"
		else: 
			return f"{ex['details']['type']} {translate(ex['details']['name'])};"

	
generated = ""
g = ""

for expr in ast:
	g += translate(expr)

for incl in includes:
	generated += "#include %s\n" % incl

generated += g
generated += "int main(){main_%s();}" % funcname

infilename = infile.split(".txt")[0]

with open("%s.cpp" % infilename,"w+") as f:
	f.write(generated)