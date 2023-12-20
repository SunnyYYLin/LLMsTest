import random
import json
import os
import re
import pyperclip
import markdown2
import webview

subject_list = ['Clang', 'Discrete Math', 'Signals and Systems']
evaluator_list = ['Huang', 'Ge', 'Lin']
lang_list = ['en', 'cn']
ai_list = ["GPT3.5", "GPT4", "ErnieBot"]
score_list = ['answer', 'thought']

class Question:   
    def __init__(self, subject, number):
        self.subject = subject
        self.number = number
        self.content = {lang: '' for lang in lang_list}
        self.image_url = ''
        self.answers = {ai: {lang: '' for lang in lang_list} for ai in ai_list}
        self.scores = {ai: {lang: {**{score_type: 0 for score_type in score_list}, 'remark': ''} for lang in lang_list} for ai in ai_list}
        self.order = -1
        self.evaluator = ''

    def __str__(self):
        return f"{{\n\t'subject': '{self.subject}',\n\t'number': '{self.number}',\n\t'content': {self.content},\n\t'image_url': '{self.image_url}',\n\t'answers': {self.answers},\n\t'scores': {self.scores}\n}}"
    
    def to_dict(self):
        return {
            'subject': self.subject,
            'number': self.number,
            'content': self.content,
            'image_url': self.image_url,
            'answers': self.answers,
            'scores': self.scores,
            'order': self.order,
            'evaluator': self.evaluator
        }
        
    def to_txt(self):
        en_text = f"You are an expert of {self.subject}. Now I have a question about {self.subject}:\n{self.content['en']}\nProvide a step-by-step answer that covers all aspects of this question and all formulas you use. It's very important to have a complete and singular answer. Thanks!"
        cn_text = f"你是{self.subject}的专家。现在我有个关于{self.subject}的问题：\n{self.content['cn']}\n提供一个逐步回答，覆盖这个问题的所有方面和你使用的所有公式。请确保回答完整并给出一个明确答案。谢谢！"
        return {"en": en_text, "cn": cn_text}
    
    @staticmethod
    def to_Question(dict):
        question = Question(dict['subject'], dict['number'])
        question.content = dict['content']
        question.image_url = dict['image_url']
        question.answers = dict['answers']
        return question
 
    @staticmethod
    def read_from_json(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            questions = json.load(file)
            questions = [Question.to_Question(question) for question in questions]
        return questions
    
    @staticmethod
    def write_to_json(questions, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            questions_dict = [question.to_dict() for question in questions]
            json.dump(questions_dict, file, ensure_ascii=False, indent=4)
            
    @staticmethod
    def write_to_md(questions, filename):
        questions = [question.to_dict() for question in questions]
        with open(filename, 'w', encoding='utf-8') as file:
            for question in questions:
                file.write(f'# {question['order']}\t{question['subject']}\t{question['number']}\n')
                file.write('## Question\n')
                file.write(f'{question['content']["cn"]}\n')
                file.write('## Answers\n')
                for ai, answer in question['answers'].items():
                    file.write(f'### {ai}\n')
                    file.write(f'{answer['en']}\n')
                    file.write('---\n')
                    file.write(f'{answer['cn']}\n')
                file.write('---\n')

    @staticmethod
    def generate_random_sequences(total_number, chapter_numbers):
        all_sequences = []
        for chapter, num_questions in chapter_numbers.items():
            for question_num in range(1, num_questions + 1):
                all_sequences.append(f"{chapter}-{question_num}")

        return random.sample(all_sequences, min(total_number, len(all_sequences)))

    @staticmethod
    def sort_sequences(sequences):
        def sort_key(sequence):
            chapter, subsequence = sequence.split('-')
            chapter_parts = chapter.split('-')
            return [int(part) for part in chapter_parts] + [int(subsequence)]

        return sorted(sequences, key=sort_key)

    @staticmethod
    def random_sequences():
        total_number = int(input("Enter total number: "))
        chapter_numbers = {}

        while True:
            input_data = input('Enter chapter and number of questions or END to finish(format:"2:43 or 2-3:23"):\n')
            if input_data == "END":
                break
            chapter, num_questions = input_data.split(":")
            chapter_numbers[chapter] = int(num_questions)

        selected_sequences = Question.generate_random_sequences(total_number, chapter_numbers)
        sorted_sequences = Question.sort_sequences(selected_sequences)

        print("Selected sequences have been written to selected_sequences.txt")
        return sorted_sequences
    
    @staticmethod
    def write_random_questions_to_json():
        for subject in subject_list:
            print(f"Processing {subject}...")
            sorted_sequences = Question.random_sequences()
            questions = []
            for sequence in sorted_sequences:
                question = Question(subject, sequence)
                questions.append(question)
                
        Question.write_to_json(questions, f'selected_questions.json')
        
    @staticmethod
    def random_order(questions):
        existed_orders = ()
        for question in questions:
            while (order := random.randint(0, len(questions))) in existed_orders:
                pass
            question.order = order
            existed_orders += (order,)
        
        return sorted(questions, key=lambda question: question.order)
    
    @staticmethod
    def questions_by_subjects(questions):
        questions_by_subjects = {subject: [] for subject in subject_list}
        for question in questions:
            questions_by_subjects[question.subject].append(question)
        if len(questions_by_subjects) != len(subject_list):
            raise ValueError("Questions are not complete.")
        return questions_by_subjects
    
    @staticmethod
    def scores_by_ais(questions):
        questions = [question.to_dict() for question in questions]
        questions_by_ais = {ai: [] for ai in ai_list}
        for question in questions:
            scores = question['scores']
            for ai in ai_list:
                questions_by_ais[ai].append(scores[ai])
        if len(questions_by_ais) != len(ai_list):
            raise ValueError("Questions are not complete.")
        return questions_by_ais
    
def distribute_questions(filename_input, filename_output):
    evaluator_number = len(evaluator_list)
    questions = Question.read_from_json(filename_input)
    questions_by_subjects = Question.questions_by_subjects(questions)
    offset = 0
    for subject, questions in questions_by_subjects.items():
        questions= Question.random_order(questions)
        for i, question in enumerate(questions):
            question.evaluator = evaluator_list[i % evaluator_number]
            question.order += offset
        questions_by_subjects[subject] = questions
        offset += len(questions)

    with open(filename_output, 'w', encoding='utf-8') as file:
        json.dump([question.to_dict() for questions in questions_by_subjects.values() for question in questions], file, ensure_ascii=False, indent=4)
        
    return questions

def answer(ai):
    max_i = max_index(ai)
    
    with open(f'merged_{ai}.json', 'r', encoding='utf-8') as file:
        questions = json.load(file)
        questions = Question.to_Question(questions)

    for i in range(max_i + 1, len(questions)):
        if max_i > -1:
            with open(f'merged_{ai}_{i-1}.json', 'r', encoding='utf-8') as file:
                questions = json.load(file)
        
        print(f'\n\n\nQuestion {i+1}:')
        question = questions[i]
        
        if question['image_url']:
            print(f'\nwith picture: {question['image_url']}')
        else:
            question_txts = Question.to_Question(question).to_txt()
            
            pyperclip.copy(question_txts['en'])
            print(f'\n{question_txts['en']}')
            en_answer = read_multiline_input("\nQuestion has been copied. Enter your answer in English: \n")
            question['answers'][ai]['en'] = en_answer

            pyperclip.copy(question_txts['cn'])
            print(f'\n{question_txts['cn']}')
            cn_answer = read_multiline_input("\n问题已经复制到剪切板。请输入您的答案（中文）: \n")
            question['answers'][ai]['cn'] = cn_answer

            questions[i] = question

        with open(f'merged_{ai}_{i}.json', 'w', encoding='utf-8') as file_to_write:
            json.dump(questions, file_to_write, ensure_ascii=False, indent=4)
        
        print(f'Updated successfully in merged_{ai}_{i}.json')
        
    print("All questions have been answered.")
    
def evaluate(filename, evaluator):
    max_i = max_index(evaluator)
    num = max_i
    
    with open(filename, 'r', encoding='utf-8') as file:
        questions = json.load(file)
        
    for i in range(max_i + 1, len(questions)):
        if max_i > -1:
            with open(f'scored_{evaluator}_{i-1}.json', 'r', encoding='utf-8') as file:
                questions = json.load(file)
                
        question = questions[i]
        if question['evaluator'] == evaluator:
            questions[i] = score(question)
        with open(f'scored_{evaluator}_{i}.json', 'w', encoding='utf-8') as file_to_write:
            json.dump(questions, file_to_write, ensure_ascii=False, indent=4)
            print(f'Updated successfullyin scored_{evaluator}_{i}.json')
        
    print("All questions have been evaluated.")
    
def merge_results(filename_output, *filenames):
    merged_questions = []
    questions = []
    
    for filename in filenames:
        with open(filename, 'r', encoding='utf-8') as file:
            questions += json.load(file)
        
    length = len(questions)//len(filenames)
    for evaluator in evaluator_list:
        index = evaluator_list.index(evaluator)
        offset = length*index
        seg = questions[offset: offset+length]
        for question in seg:
            if question['evaluator'] == evaluator:
                merged_questions.append(question)
        
    with open(filename_output, 'w', encoding='utf-8') as file:
        json.dump(merged_questions, file, ensure_ascii=False, indent=4)
        
    return merged_questions
        
def score(question):
    if question != None:
        print(f"Evaluating: {question['subject']} {question['number']} by {question['evaluator']}")
        if question['image_url']:
            print(f'\nwith picture: {question['image_url']}')
        else:
            answers = [(ai, ai_answer) for ai, ai_answer in question['answers'].items()]
            random.shuffle(answers)
            
            for answer in answers:
                ai, ai_answer = answer
                show(ai_answer, question, len(answers))
                for lang, answer in ai_answer.items():
                    score = {}
                    for score_type in score_list:
                        while True:
                            try:
                                score[score_type] = float(input(f'Score for answer in {len(answers)} for {score_type}:'))
                                if 0<=score[score_type]<=10:
                                    break
                                print('ValueError!')
                            except ValueError:
                                print("ValueError!")
                                pass
                    score['remark'] = input(f'Remark for answer in {len(answers)}:')
                    question['scores'][ai][lang] = score
                
    return question

def show(ai_answer, question, total):
    answer_md = question['subject']+question['number']+question['content']['cn']
    for lang, answer in ai_answer.items():
        answer_md += f'# {lang}\n'+f'{answer}\n'+'---\n'
    html_content = str(markdown2.markdown(answer_md))
    webview.create_window(f'Answer in {total}', html=html_content)
    webview.start()
        
def max_index(name):
    path = '.'
    files = os.listdir(path)
    pattern = rf'scored_{name}_(\d+).json'
    max_i = -1
    
    for file in files:
        match = re.search(pattern, file)
        if match:
            i = int(match.group(1))
            if i > max_i:
                max_i = i
    
    return max_i

def read_multiline_input(prompt):
    print(prompt)
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
    return "\n".join(lines)

def sort_questions_by_number(questions):
    sequences = [question.number for question in questions]
    sequences = Question.sort_sequences(sequences)
    

if __name__ == "__main__":
    questions = Question.read_from_json('merged.json')
    results_by_ais = Question.scores_by_ais(questions)
    with open('results_by_ais.json', 'w', encoding='utf-8') as file:
        json.dump(results_by_ais, file, ensure_ascii=False, indent=4)