# Boilerplate
from os.path import dirname, join
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from pylatex import Document, Section, Subsection, Figure, SubFigure, NoEscape, Command
from pdflatex import PDFLaTeX

# Specify paths
project_root = dirname(dirname(__file__))
data_path = join(project_root, 'data/apple-news-daily-crossword-data.csv')
# compiler_path = join(project_root, '/venv/lib/python3.10/site-packages/pdflatex')

# Read data to Pandas DataFrame
df = pd.read_csv(data_path, encoding = 'utf8')

# Convert 'time_to_complete' to 'duration'
df['duration'] = df['time_to_complete'].apply(lambda x: dt.timedelta(minutes = dt.time.fromisoformat(x).minute, seconds = dt.time.fromisoformat(x).second).seconds)

# Group by Player
df_grouped = df.pivot_table(values = 'duration', 
                            index = ['crossword_date', 'first_name']).reset_index()

# LaTeX
def main_document(fname, width, project_root, *args, **kwargs):
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
        doc.append("The FAFO method demonstrates that Graeme is less skilled than Kelly when it comes to rapidly solving crossword puzzles.")

    # Analysis
    with doc.create(Section('Analysis')):
        
        with doc.create(Subsection('Performance Comparison')):
            doc.append("As evidenced by the plots below, Kelly's superior ability to kick ass and take names is apparent at a glance.")
            with doc.create(Figure(position = 'htbp')) as plot:
                with doc.create(SubFigure()) as subplot:
                    # Performance over Time
                    subplot.add_caption('Completion Duration by Date')
                    plt.figure(figsize = (6, 3.5))
                    fig_1 = sns.lineplot(data = df_grouped,
                                        x = 'crossword_date',
                                        y = 'duration',
                                        hue = 'first_name',
                                        legend = True)
                    plt.xticks(rotation = 90)
                    yticks = fig_1.get_yticks()
                    fig_1.set_yticklabels(pd.to_datetime(yticks, unit = 's').strftime('%H:%M:%S'))
                    # plt.title('Apple News+ Daily Crossword Completion Times')
                    plt.legend(title = 'Player')
                    plt.xlabel('Crossword Date')
                    plt.ylabel('Duration')
                    plt.tight_layout()
                    subplot.add_plot(width = NoEscape(width))

                with doc.create(SubFigure()) as subplot:
                    # Performance distribution
                    subplot.add_caption('Distribtution of Durations by Player')
                    plt.figure(figsize = (6, 3.5))
                    fig_2 = sns.boxplot(data = df_grouped,
                                        x = 'first_name',
                                        y = 'duration',
                                        hue = 'first_name',
                                        legend = True)
                    yticks = fig_2.get_yticks()
                    fig_2.set_yticklabels(pd.to_datetime(yticks, unit = 's').strftime('%H:%M:%S'))
                    # plt.title('Apple News+ Daily Crossword Completion Distribution')
                    plt.legend(title = 'Player')
                    plt.xlabel('Player')
                    plt.ylabel('Duration')
                    plt.tight_layout()
                    subplot.add_plot(width = NoEscape(width))
                

    # Conclusion
    with doc.create(Section('Conclusion')):
        doc.append("Graeme fucked around and found out...though he found out that he sucks at crossword puzzles.")

    # Generate .pdf
    doc.generate_tex()
    tex_file = join(project_root, f'{fname}.tex')
    pdfl = PDFLaTeX.from_texfile(tex_file)
    pdf = pdfl.create_pdf(keep_pdf_file = True)


if __name__ == '__main__':
    main_document(fname = 'apple-news-plus-daily-crossword-performance-analysis', 
                  width = r'1\textwidth', 
                  project_root= project_root,
                  dpi=300)
