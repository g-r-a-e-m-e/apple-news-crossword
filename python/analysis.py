# Boilerplate
from os.path import dirname, join
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from pylatex import Document, Section, Subsection, Figure, NoEscape, Command

# Specify data path
project_root = dirname(dirname(__file__))
path = join(project_root, 'data/apple-news-daily-crossword-data.csv')

# Read data to Pandas DataFrame
df = pd.read_csv(path, encoding = 'utf8')

# Convert 'time_to_complete' to 'duration'
df['duration'] = df['time_to_complete'].apply(lambda x: dt.timedelta(minutes = dt.time.fromisoformat(x).minute, seconds = dt.time.fromisoformat(x).second).seconds)

# Group by Player
df_grouped = df.pivot_table(values = 'duration', 
                            index = ['crossword_date', 'first_name']).reset_index()

# LaTeX
def main_document(fname, width, *args, **kwargs):
    # Document geometry
    geometry_options = {"top": "2cm", "bottom": "2cm", "right": "2cm", "left": "2cm"}
    # Create document
    doc = Document(fname, geometry_options = geometry_options)
    # Specify Preamble
    doc.preamble.append(Command('title', 'Apple News+ Daily Crossword Performance Analysis'))
    doc.preamble.append(Command('author', 'Graeme Benson'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.append(NoEscape(r'\maketitle'))
    # Sections
    # Abstract
    with doc.create(Section('Abstract')):
        doc.append("The FAFO method demonstrates that Graeme is not as skilled as Kelly when it comes to rapidly solving crossword puzzles.")

    # Analysis
    with doc.create(Section('Analysis')):
        
        with doc.create(Subsection('Performance Over Time')):
            doc.append("As evidenced by the plot below, Graeme sucks at crossword puzzles. Kelly's superior ability to kick ass and take names is apparent at a glance.")
            with doc.create(Figure(position = 'htbp')) as plot:
                sns.set(font_scale = 0.5)
                # Performance over Time
                plt.figure(figsize = (6, 3.5))
                fig_1 = sns.lineplot(data = df_grouped,
                                     x = 'crossword_date',
                                     y = 'duration',
                                     hue = 'first_name',
                                     legend = True)
                plt.xticks(rotation = 30)
                yticks = fig_1.get_yticks()
                fig_1.set_yticklabels(pd.to_datetime(yticks, unit = 's').strftime('%H:%M:%S'))
                plt.title('Apple News+ Daily Crossword Completion Times')
                plt.legend(title = 'Player')
                plt.xlabel('Crossword Date')
                plt.ylabel('Duration')
                plt.tight_layout()
                plot.add_plot(width = NoEscape(width))
                plot.add_caption('Completion Duration by Date')
                doc.append('Created using matplotlib.')

    # Conclusion
    with doc.create(Section('Conclusion')):
        doc.append("Graeme fucked around and found out...though he found out that he sucks at crossword puzzles.")

    # Generate .pdf using local compiler
    doc.generate_pdf(clean_tex = False, 
                     compiler = '/usr/local/texlive/2023/bin/universal-darwin/pdflatex')

if __name__ == '__main__':
    main_document('apple-news-plus-daily-crossword-performance-analysis', r'.75\textwidth', dpi=300)
