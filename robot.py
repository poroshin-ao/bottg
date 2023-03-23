symbols = [' ', 'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к',
           'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч',
           'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']


def str_to_robot(mes: str, ans: str):
    if len(mes) > 40:
        return "Err"
    s = ''
    mes = mes.lower()
    ans = ans.lower()
    for i in range(len(mes)):
        if mes[i] in symbols and i < len(ans):
            if symbols.index(mes[i]) < symbols.index(ans[i]):
                s += '0'
            else:
                s += '1'
        else:
            s += '1'
    return s
