import jieba
from collections import Counter

# 需要分词的中文文本
text = "结巴分词是一款优秀的中文分词工具，功能强大且易于使用。结巴分词可以应用于文本处理、信息检索等多个领域。是事实是吗"

# 加载停用词表
stopwords = set()
with open("./utils/baidu_stopwords.txt", "r", encoding="utf-8") as f:
    for line in f:
        stopwords.add(line.strip())

# 使用jieba进行分词
seg_list = jieba.cut(text, cut_all=False)
print("************")
print(seg_list)

# 将分词结果转换为列表，并去除停用词
seg_list = [word for word in seg_list if word not in stopwords]
print("************")
print(seg_list)

# 对去除停用词后的分词结果进行词频统计
word_count = Counter(seg_list)

# 输出词频统计结果
print("去除停用词后的词频统计结果：")
for word, count in word_count.items():
    print(word, ":", count)
