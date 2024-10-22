import pandas as pd
import numpy as np

# 设置随机种子保证结果可重复
np.random.seed(42)

# 数据大小
n = 100000

# 随机生成数据特征
data = {
    'customer_id': np.arange(1, n + 1),
    'age': np.random.randint(18, 80, n),
    'gender': np.random.choice(['Male', 'Female'], n, p=[0.48, 0.52]),
    'policy_type': np.random.choice(['Basic', 'Premium', 'Comprehensive'], n, p=[0.5, 0.3, 0.2]),
    'years_with_company': np.random.randint(1, 21, n),
    'num_claims': np.random.poisson(1.5, n).clip(0, 15),
    'annual_premium': np.round(np.random.normal(7000, 2000, n).clip(500, 30000), 2),
    'customer_complaints': np.random.poisson(0.5, n).clip(0, 10),
    'auto_renewal': np.random.choice([0, 1], n, p=[0.2, 0.8]),
    'has_life_insurance': np.random.choice([0, 1], n, p=[0.6, 0.4]),
    'family_size': np.random.randint(1, 6, n)
}

# 生成逻辑流失标签：根据业务规则和特征生成更合理的流失标签
def generate_churn(row):
    if (row['policy_type'] == 'Basic' and row['num_claims'] > 3 and
        row['customer_complaints'] > 2 and row['auto_renewal'] == 0):
        return 1  # 高风险流失
    elif row['years_with_company'] > 5 and row['auto_renewal'] == 1:
        return 0  # 低风险不流失
    else:
        return np.random.choice([0, 1], p=[0.75, 0.25])  # 加入随机性

# 创建 DataFrame 并添加流失标签
df = pd.DataFrame(data)
df['churn'] = df.apply(generate_churn, axis=1)

# 检查生成的数据
print(df.head())

# 保存为CSV文件
df.to_excel('insurance_data.xlsx', index=False)
print("数据已保存至 'insurance_data.xlsx'")
