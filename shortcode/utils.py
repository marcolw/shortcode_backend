import re


def resolveReferences(value, organizedProductData):
    if -1 != value.find('^'):
        arr = value.split('^')
        for i in range(1, len(arr), 2):
            ps = arr[i].split(':')

            if len(ps) < 2:
                continue

            ps[0] = ps[0].strip()
            ps[1] = ps[1].strip()

            if ps[0] in organizedProductData and organizedProductData[ps[0]]:
                if ps[1] in organizedProductData[ps[0]]:
                    value = value.replace(
                        f'^{arr[i]}^', f'{organizedProductData[ps[0]][ps[1]]}')
                else:
                    value = value.replace(f'^{arr[i]}^', "")

    return value


def getRenderedText(value, data, organizedProductData):
    if not isinstance(value, str) or len(value) == 0:
        return ''

    value = resolveReferences(value, organizedProductData)

    if value.find('#') != -1:
        # replace html color values
        # [a-zA-Z0-9]{3,6};
        value = re.sub('#([a-fA-F0-9]{3,6});', "*c*o*l*\\1;", value)
        arr = value.split('#')

        for i in range(1, len(arr), 2):
            ps = arr[i].split(';')
            prefix = ''

            ps[0] = ps[0].strip()

            # todo: include or endsWith?
            if arr[i].find('!') != -1:
                tmp = re.sub("_x(.*)x$", " (\\1)", ps[0]).replace("_", " ")
                prefix = f'{tmp}: '

            if -1 == arr[i].find("UM"):
                if data:
                    if ps[0] in data:
                        if type(data[ps[0]]) == list:
                            if None in data[ps[0]]:
                                print(
                                    f'{data["sku"]}: while rendering <{value}>, <{data[ps[0]]}> contains None object.')
                            data[ps[0]] = list(map(str, data[ps[0]]))
                            value = value.replace(
                                f'#{arr[i]}#', f'{prefix}{", ".join(data[ps[0]])}')
                        else:
                            value = value.replace(
                                f'#{arr[i]}#', f'{prefix}{data[ps[0]]}')
                    else:
                        value = value.replace(f'#{arr[i]}# ', "")
                        value = value.replace(f'#{arr[i]}#', "")

            elif len(ps) >= 2:
                res = re.search("_x(.*)x$", ps[0])

                if len(ps) > 2 and ps[2].find('UM') != -1:
                    ps[1] = ps[2]

                if res:
                    ps[1] = ps[1].replace("UM", res.group(1))
                else:
                    ps[1] = ps[1].replace("UM", "")

                if data:
                    if ps[0] in data:
                        if type(data[ps[0]]) == list:
                            if None in data[ps[0]]:
                                print(
                                    f'{data["sku"]}: while rendering <{value}>, <{data[ps[0]]}> contains None object.')
                            data[ps[0]] = list(map(str, data[ps[0]]))
                            value = value.replace(
                                f'#{arr[i]}#', f'{prefix}{", ".join(data[ps[0]])}{ps[1]}')
                        else:
                            value = value.replace(
                                f'#{arr[i]}#', f'{prefix}{data[ps[0]]}{ps[1]}')
                    else:
                        value = value.replace(f'#{arr[i]}# ', "")
                        value = value.replace(f'#{arr[i]}#', "")
        # restore html color values
        value = value.replace('*c*o*l*', "#")

    if value.find('^') != -1:
        arr = value.split('^')

        for i in range(1, len(arr), 2):
            ps = arr[i].split(';')
            prefix = ''

            if arr[i].find("UM") == -1:
                if len(ps) < 2:
                    continue

                ps[0] = ps[0].strip()
                ps[1] = ps[1].strip()

                # todo: include or endsWith?
                if arr[i].find('!') != -1:
                    tmp = re.sub("_x(.*)x$", " (\\1)", ps[1]).replace("_", " ")
                    prefix = f'{tmp}: '

                if ps[0] in organizedProductData and organizedProductData[ps[0]]:
                    if ps[1] in organizedProductData[ps[0]]:
                        if type(organizedProductData[ps[0]][ps[1]]) == list:
                            if None in organizedProductData[ps[0]][ps[1]]:
                                print(
                                    f'{data["sku"]}: while rendering <{value}>, <{organizedProductData[ps[0]][ps[1]]}> contains None object.')
                            organizedProductData[ps[0]][ps[1]] = list(
                                map(str, organizedProductData[ps[0]][ps[1]]))
                            value = value.replace(
                                f'^{arr[i]}^', f'{prefix}{", ".join(organizedProductData[ps[0]][ps[1]])}')
                        else:
                            value = value.replace(
                                f'^{arr[i]}^', f'{prefix}{organizedProductData[ps[0]][ps[1]]}')
                    else:
                        value = value.replace(f'^{arr[i]}^ ', "")
                        value = value.replace(f'^{arr[i]}^', "")

            elif len(ps) >= 3:
                ps[0] = ps[0].strip()
                ps[1] = ps[1].strip()

                # todo: include or endsWith?
                if arr[i].find('!') != -1:
                    tmp = re.sub("_x(.*)x$", " (\\1)", ps[1]).replace("_", " ")
                    prefix = f'{tmp}: '

                if len(ps) > 3 and ps[3].find('UM') != -1:
                    ps[2] = ps[3]

                res = re.search("_x(.*)x$", ps[1])
                if res:
                    ps[2] = ps[2].replace("UM", res.group(1))
                else:
                    ps[2] = ps[2].replace("UM", "")

                if ps[0] in organizedProductData and organizedProductData[ps[0]]:
                    if ps[1] in organizedProductData[ps[0]]:
                        if type(organizedProductData[ps[0]][ps[1]]) == list:
                            if None in organizedProductData[ps[0]][ps[1]]:
                                print(
                                    f'{data["sku"]}: while rendering <{value}>, <{organizedProductData[ps[0]][ps[1]]}> contains None object.')
                            organizedProductData[ps[0]][ps[1]] = list(
                                map(str, organizedProductData[ps[0]][ps[1]]))
                            value = value.replace(
                                f'^{arr[i]}^', f'{prefix}{", ".join(organizedProductData[ps[0]][ps[1]])}{ps[2]}')
                        else:
                            value = value.replace(
                                f'^{arr[i]}^', f'{prefix}{organizedProductData[ps[0]][ps[1]]}{ps[2]}')
                    else:
                        value = value.replace(f'^{arr[i]}^ ', "")
                        value = value.replace(f'^{arr[i]}^', "")

    return value
