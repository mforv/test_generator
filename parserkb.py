from json import dump, dumps
from re import findall, match
from random import randint
def load_kb(filename = "kb.txt"):
	res = {}
	for str in open("kb.txt").readlines():
		try:
			a, b, c = findall(r'.*?"(.*?)".*?"(.*?)".*?"(.*?)".*', str.lower())[0]
			res.update({(a,c,b):1})
		except ValueError:
			pass
		except TypeError:
			pass
		except IndexError:
			pass
	return res

def generate_questions(kb = {}, number = 10):
	def what_includes(text, den1, rel, den2):
		def generate_answers(den1, rel, den2, n_incorrect = 3, n_correct = 1):
			var = 'а'
			res = {}
			keys_to_delete = []
			for i in range(n_correct):
				correct = []
				for d1, r, d2 in kb.keys():
					if d1 == den1 and r == rel:
						correct += [d2]
						keys_to_delete += [(d1, r, d2)]
				res.update({var:{"is_correct":1, "text": ', '.join(correct)}})
				var = chr(ord(var)+1)

			incorrect = []
			a, b = 0, 0
			for d1, r, d2 in kb.keys():
				if d1 != den1 and r == rel:
					incorrect += [d2]
					keys_to_delete += [(d1, r, d2)]
					if a and b and randint(1,3) > 1:
						res.update({var:{"is_correct":0, "text": ', '.join(incorrect)}})
						var = chr(ord(var)+1)
						incorrect = []
					if not a: a = 1
					if a and not b: b = 1
			for key in set(keys_to_delete):
				del kb[key]
			return res

		def generate_question(den, template):
			for den1, rel, den2 in kb.keys():
				if den2 == den:
					return template % (den, den1)
		q = generate_question(den1, templ_key)
		answers = generate_answers(den1, rel, den2)
		return {"%s) %s" % (i, q):answers}

	question_templates = {
		"%s это:" : (""),
		"Что включает в себя %s, как элемент %s" : {
			"function" : what_includes,
			"relations" : (r"представлять собой"),
			"weight": 1,
		},
		"%s состоит из" : 1,
		"%s определяется как" : 1,
	}
	res = {}
	for i in range(1,number + 1):
		templ_key = "Что включает в себя %s, как элемент %s" # question_templates.keys[0]
		templ_relation_re = question_templates[templ_key]["relations"][0]
		for den1, rel, den2 in kb.keys():
			if match(templ_relation_re, rel):
				res.update(question_templates[templ_key]["function"](templ_key, den1, rel, den2))
				break
	return res

if __name__ == '__main__':
	kb = load_kb("kb.txt")
	q = generate_questions(kb, 10)
	# print(q)
	dump(q, open('q.json', 'w'), ensure_ascii = 0, indent = 4)
	print(dumps(q, ensure_ascii = 0, indent = 4))
