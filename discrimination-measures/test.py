from discrimination import analyze

def main():
    analyzer = analyze.Dataset('adult-data.csv', ['<=50K', '>50K'])
    analyzer.init_protected({'race' : 'Black'})

    print("Risk Ratio " + str(analyzer.risk_ratio()))
    print("Risk Difference  " + str(analyzer.risk_diff()))
    print("Relative Chance: " + str(analyzer.rel_chance()))

    print(analyzer.get_avg_consistency(200, 5, .005))

main()
