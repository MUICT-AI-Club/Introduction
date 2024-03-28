import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud, STOPWORDS

df = pd.read_csv("ICT faculty AI club registeration form (Responses) - Sheet1.csv")

def student_id_cleaning(s):
    if s[0] == 'u':
        return s[1:]
    return s
def extract_year(s):
    aca_year = s[0:2]
    if aca_year == "63":
        return "4"
    if aca_year == "64":
        return "3"
    if aca_year == "65":
        return "2"
    if aca_year == "66":
        return "1"
n_students = df.shape[0]
student_id = df["รหัสนักศึกษา (Student ID)"].astype(str).apply(student_id_cleaning)
student_year = student_id.apply(extract_year)
student_year_value_count = student_year.value_counts(sort=False)
student_year_value_count_relative = student_year_value_count / n_students

plt.figure()
plt.title("Student year")
plt.pie(student_year_value_count.values, labels=[f"Year {y}, n = {n} ({r*100:.2f}%)" for (y, n, r) in zip(student_year_value_count.index, student_year_value_count.values, student_year_value_count_relative.values)], colors=["dodgerblue", "yellow", "lightpink", "springgreen"], shadow=True)
plt.savefig("year_piechart.png", transparent=True)
plt.close()

expertise = ""
for exp in df.iloc[:, 7]:
    for s in exp.split(","):
        if s == "ไม่มี":
            s = "None"
        expertise += (s.strip().lower() + ",")
expertise_splited = pd.Series(expertise.split(",")).value_counts()
print(expertise_splited)
plt.figure()
plt.barh(expertise_splited.index, expertise_splited.values)
# plt.xticks(rotation=90)
plt.xlabel("Number of people")
plt.title("Number of people who has expertise in each topic")
plt.subplots_adjust(left=0.3)
plt.savefig("expertise_bar.png", transparent=True)
plt.close()


for year in student_year.unique():
    expertise_each_year = df.loc[student_year == year].iloc[:, 7]
    expertise = ""
    for exp in expertise_each_year:
        for s in exp.split(","):
            if s == "ไม่มี":
                s = "None"
            expertise += (s.strip().lower() + ",")
    expertise_splited = pd.Series(expertise.split(",")).value_counts()
    print(expertise_splited)    
    plt.figure()
    plt.barh(expertise_splited.index, expertise_splited.values)
    # plt.xticks(rotation=90)
    plt.xlabel("Number of people")
    plt.title(f"year {year} student who has expertise in each topic")
    plt.subplots_adjust(left=0.3)
    plt.savefig(f"expertise_bar_year{year}.png", transparent=False)
    plt.close()


text = ""
for t in df.iloc[:, 7]:
    text += t + " "
word_cloud = WordCloud(font_path="THSarabunNew.ttf", collocations = False, background_color = 'white').generate(text)
plt.imshow(word_cloud, interpolation='bilinear')
plt.axis("off")
plt.show()
