from ipywidgets import interact, fixed, FloatSlider, IntSlider, HBox, VBox, interactive_output, Layout, GridspecLayout, ToggleButton
from IPython.display import display, Latex
import ipywidgets as widget
import json, pandas
import random as rnd

QUESTION_SET_FILE = 'Quiz/question_sheet.csv'

class MultipleChoiceQuestion:
    def __init__(self, question_text="", alternatives=[]):

        self.question_text = question_text
        self.alternatives = alternatives
        self.student_answer = ""
        #rnd.shuffle(self.alternatives)
        self.N = len(self.alternatives)
        self.selected = None
        self.taskID = ""
        
    def save(self, taskID):
        # Create dictionary from member variables
        file_data = {'question_text': self.question_text,
                     'alternatives': self.alternatives,
                     'student_answer': self.student_answer
                    }
        self.taskID = taskID
        # Encode member variables
        data_string = json.dumps(file_data)
        
        # Load existing file or create new file
        try:
            df = pandas.read_csv(QUESTION_SET_FILE, index_col='taskID')
        except FileNotFoundError:
            # Clear data file. Find a way to not have to do this manually
            df = pandas.DataFrame({'type': [], 'data': []})
            df.index.name = 'taskID'
        df.loc[taskID] = ['MultipleChoice', data_string]
        df.sort_index()
        df.to_csv(QUESTION_SET_FILE)
        
    def get_task(self, taskID):
        self.taskID = taskID
        df = pandas.read_csv(QUESTION_SET_FILE, index_col='taskID')
        if taskID in df.index:
            if df.loc[taskID]['type']=='MultipleChoice':
                data_string = df.loc[taskID]['data']
                file_data = json.loads(data_string)
                self.question_text = file_data['question_text']
                self.alternatives = file_data['alternatives']
                self.student_answer = file_data['student_answer']
                self.N = len(self.alternatives)
                
    def updateSelection(self, clickedButton):
        if(self.selected):
            self.selected.button_style = ''
            if(self.selected == clickedButton):
                self.selected = None
                self.student_answer = ""
            else:
                clickedButton.button_style = 'info'
                self.selected = clickedButton
                self.student_answer = clickedButton.description
        else:
            clickedButton.button_style = 'info'
            self.selected = clickedButton
            self.student_answer = clickedButton.description
        self.save(self.taskID)
        

    

    def show(self):
        #self.out2 = interactive_output(self.checkAnswer,  {'checkButton':self.checkButton})
        display(Latex(self.question_text))
        
        # Set up button panel for answers
        buttonText = [self.alternatives[i] for i in range(self.N)]
        self.grid = GridspecLayout(1, self.N, width='100%')
        for i, label in enumerate(buttonText):
            self.grid[0,i] = widget.Button(description=label, layout=Layout(height='50px', width='auto'))

        #self.checkButton = widget.Button(description="Check Solution:", button_style='warning', layout=Layout(height='50px', width='50%'))
        #self.feedback = widget.Output(layout={'border': '1px solid black', 'width':'50%'})
        #self.feedbackPanel = HBox([self.checkButton, self.feedback])

        for i in range(self.N):
            self.grid[0,i].on_click(self.updateSelection)
        #self.checkButton.on_click(self.checkAnswer)         
        
        display(self.grid)
                 
        if self.student_answer != "":
            for index in range(self.N):
                if self.grid[0,index] == self.student_answer:
                    self.grid[0,index].button_style = 'info'
                    self.selected = self.grid[0,index]
                        
        #display(self.feedbackPanel)
        
    def load(self, taskID):
        self.get_task(taskID)
        self.show()