# Boilerplate
from os.path import dirname, join
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import datetime as dt
from pylatex import Document, Section, Subsection, Figure, SubFigure, NoEscape, NewLine, Command
from pdflatex import PDFLaTeX

# Specify paths
project_root = dirname(dirname(__file__))
data_path = join(project_root, 'data/apple-news-daily-crossword-data.csv')

# Read data to Pandas DataFrame
df = pd.read_csv(data_path, encoding = 'utf8')

# Convert 'time_to_complete' to 'duration'
df['duration'] = df['time_to_complete'].apply(lambda x: dt.timedelta(minutes = dt.time.fromisoformat(x).minute, seconds = dt.time.fromisoformat(x).second).seconds)

# Create Day of Week dummy variables
df['crossword_day_of_week'] = df['crossword_date'].apply(lambda x: dt.date.fromisoformat(x).strftime('%A'))
df['completion_day_of_week'] = df['date_completed'].apply(lambda x: dt.date.fromisoformat(x).strftime('%A'))
df['average_duration_per_word'] = df['duration'] / df['word_count']

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
    ## Abstract
    with doc.create(Section('Abstract')):
        doc.append("The FAFO method demonstrates that Graeme is less skilled than Kelly when it comes to rapidly solving crossword puzzles.")

    ## Analysis
    with doc.create(Section('Analysis')):
        with doc.create(Subsection('Performance Comparison')):
            doc.append("As evidenced by the plots below, Kelly's superior ability to kick ass and take names is apparent at a glance.")
            
            with doc.create(Figure(position = 'h!')) as plot:
                # Performance over time
                with doc.create(SubFigure(position = 'c', width = NoEscape(r'.45\linewidth'))) as subplot:
                    subplot.add_caption('Completion Duration by Date')
                    plt.figure(figsize = (6, 3.5))
                    fig = sns.lineplot(data = df,
                                        x = 'crossword_date',
                                        y = 'duration',
                                        hue = 'first_name',
                                        legend = True)
                    plt.xticks(rotation = 90)
                    yticks = fig.get_yticks()
                    fig.set_yticklabels(pd.to_datetime(yticks, unit = 's').strftime('%H:%M:%S'))
                    labels = [dt.date.fromisoformat(i).strftime('%b-%d') for i in df['crossword_date'].unique()]
                    xticks = fig.get_xticks()
                    plt.xticks(ticks = xticks, labels = labels)
                    plt.legend(title = 'Player')
                    plt.xlabel('Crossword Date')
                    plt.ylabel('Duration')
                    plt.tight_layout()
                    subplot.add_plot()

                # Performance distribution
                with doc.create(SubFigure(position = 'c', width = NoEscape(r'.45\linewidth'))) as subplot:
                    subplot.add_caption('Distribtution of Durations by Player')
                    plt.figure(figsize = (6, 3.5))
                    fig = sns.boxplot(data = df,
                                        x = 'first_name',
                                        y = 'duration',
                                        hue = 'first_name',
                                        legend = True)
                    yticks = fig.get_yticks()
                    fig.set_yticklabels(pd.to_datetime(yticks, unit = 's').strftime('%H:%M:%S'))
                    plt.legend(title = 'Player')
                    plt.xlabel('Player')
                    plt.ylabel('Duration')
                    plt.tight_layout()
                    subplot.add_plot()
            
                doc.append(NewLine())
                # Duration by Day of Week
                with doc.create(SubFigure(position = 'c', width = NoEscape(r'.45\linewidth'))) as subplot:
                    subplot.add_caption('Average Durations by Day of Week Completed')
                    plt.figure(figsize = (6, 3.5))
                    fig = sns.lineplot(data = df,
                                         x = 'completion_day_of_week',
                                         y = 'duration',
                                         hue = 'first_name',
                                         legend = True)
                    yticks = fig.get_yticks()
                    fig.set_yticklabels(pd.to_datetime(yticks, unit = 's').strftime('%H:%M:%S'))
                    plt.xticks(rotation = 45)
                    plt.legend(title = 'Player')
                    plt.xlabel('Day of Week')
                    plt.ylabel('Duration')
                    plt.tight_layout()
                    subplot.add_plot()

                # Scatterplot
                with doc.create(SubFigure(position = 'c', width = NoEscape(r'.45\linewidth'))) as subplot:
                    subplot.add_caption('Average Duration per Word')
                    plt.figure(figsize = (6, 3.5))
                    fig = sns.scatterplot(data = df,
                                        x = 'word_count',
                                        y = 'average_duration_per_word',
                                        hue = 'first_name',
                                        legend = True)
                    yticks = fig.get_yticks()
                    fig.set_yticklabels(pd.to_datetime(yticks, unit = 's').strftime('%H:%M:%S'))
                    plt.legend(title = 'Player')
                    plt.xlabel('Word Count')
                    plt.ylabel('Duration')
                    plt.tight_layout()
                    subplot.add_plot()

                # doc.append(NewLine())
                # # Boxplot
                # with doc.create(SubFigure(position = 'c', width = NoEscape(r'.45\linewidth'))) as subplot:
                #     subplot.add_caption('Durations by Time of Day')
                #     plt.figure(figsize = (6, 3.5))
                #     fig = sns.boxplot(data = df,
                #                         x = 'time_of_day_completed',
                #                         y = 'duration',
                #                         hue = 'first_name',
                #                         legend = True)
                #     yticks = fig.get_yticks()
                #     fig.set_yticklabels(pd.to_datetime(yticks, unit = 's').strftime('%H:%M:%S'))
                #     plt.legend(title = 'Player')
                #     plt.xlabel('Time of Day')
                #     plt.ylabel('Duration')
                #     plt.tight_layout()
                #     subplot.add_plot()
                
    # Conclusion
    with doc.create(Section('Conclusion')):
        doc.append("Graeme fucked around and found out...though he found out that he sucks at crossword puzzles.")

    # Generate .pdf
    doc.generate_tex()
    tex_file = join(project_root, f'{fname}.tex')
    pdfl = PDFLaTeX.from_texfile(tex_file)
    pdfl.create_pdf(keep_pdf_file = True)


if __name__ == '__main__':
    main_document(fname = 'apple-news-plus-daily-crossword-performance-analysis', 
                  width = r'\textwidth', 
                  project_root = project_root,
                  dpi=300)
