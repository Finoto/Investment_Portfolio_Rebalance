import pandas as pd
from yahoo_fin import stock_info as si

#importa carteira em Excel

carteira_atual = pd.read_csv('/Users/GustavoFinoto/desktop/carteira/CarteiraAtual.csv', sep = ';')
carteira_ideal = pd.read_csv('/Users/GustavoFinoto/desktop/carteira/CarteiraIdeal.csv', sep = ';')

#Trabalhando primeiramente com ações BR

carteira_acoesBR = carteira_atual[carteira_atual.Categoria=='Ações BR']
carteira_FII = carteira_atual[carteira_atual.Categoria=='FII']
carteira_acoesEUA = carteira_atual[carteira_atual.Categoria=='Ações EUA']
carteira_REITS = carteira_atual[carteira_atual.Categoria=='REIT EUA']


acoesBR = carteira_acoesBR['ATIVO'].tolist()
FII = carteira_FII['ATIVO'].tolist()
acoesEUA = carteira_acoesEUA['ATIVO'].tolist()
REITS = carteira_REITS['ATIVO'].tolist()


#Adicionar .SA nas ações BR

def adicionaSA():
    for i in range(len(acoesBR)):
        acoesBR[i] = acoesBR[i] + '.SA'

def adicionaSA_FII():
    for i in range(len(FII)):
        FII[i] = FII[i] + '.SA'

adicionaSA_FII()
adicionaSA()

# criar lista vazia de preços, tamanho da quantidade de ativos

preco_acoesEUA = [1]*len(acoesEUA)
preco_REITS = [1]*len(REITS)

preco_dol_acoesEUA = [1]*len(acoesEUA)
preco_dol_REITS = [1]*len(REITS)

preco_acoesBR = [1]*len(acoesBR)
preco_FII = [1]*len(FII)

def cotacao():
    for i in range(len(acoesBR)):
        preco_acoesBR[i] = round(si.get_live_price(acoesBR[i]),2)

def cotacao_FII():
    for i in range(len(FII)):
        preco_FII[i] = round(si.get_live_price(FII[i]),2)

def cotacao_acoesEUA():
    for i in range(len(acoesEUA)):
        preco_acoesEUA[i] = round(si.get_live_price(acoesEUA[i]),2)
        
def cotacao_REITS():
    for i in range(len(REITS)):
        preco_REITS[i] = round(si.get_live_price(REITS[i]),2)     

def cotacao_dol_acoesEUA():
    for i in range(len(acoesEUA)):
        preco_dol_acoesEUA[i] = round(si.get_live_price('BRL=X'),2)
        
def cotacao_dol_REITS():
    for i in range(len(REITS)):
        preco_dol_REITS[i] = round(si.get_live_price('BRL=X'),2)
        
cotacao()
cotacao_FII()
cotacao_acoesEUA()
cotacao_REITS()
cotacao_dol_acoesEUA()
cotacao_dol_REITS()

#transformar a quantidade em lista

qtd_acoesBR = carteira_acoesBR['Quantidade'].tolist()

qtd_FII = carteira_FII['Quantidade'].tolist()

qtd_acoesEUA = carteira_acoesEUA['Quantidade'].tolist()

qtd_REITS = carteira_REITS['Quantidade'].tolist()


#criar novo dataframe com todas preço, quandidade e ativo

carteira_acoesBR = pd.DataFrame(list(zip(acoesBR, qtd_acoesBR, preco_acoesBR)), columns=['Ativo', 'Qtd', 'Preço'])

carteira_FII = pd.DataFrame(list(zip(FII, qtd_FII, preco_FII)), columns=['Ativo', 'Qtd', 'Preço'])

carteira_acoesEUA = pd.DataFrame(list(zip(acoesEUA, qtd_acoesEUA, preco_acoesEUA, preco_dol_acoesEUA)), columns=['Ativo', 'Qtd', 'Preço', 'USD'])

carteira_REITS = pd.DataFrame(list(zip(REITS, qtd_REITS, preco_REITS, preco_dol_REITS)), columns=['Ativo', 'Qtd', 'Preço', 'USD'])

#calculo do valor em carteira de cada ativo

carteira_acoesBR['Valor'] = carteira_acoesBR.apply(lambda row: row.Qtd * row.Preço, axis = 1)

carteira_FII['Valor'] = carteira_FII.apply(lambda row: row.Qtd * row.Preço, axis = 1)

carteira_acoesEUA['Valor'] = carteira_acoesEUA.apply(lambda row: row.Qtd * row.Preço * row.USD, axis = 1)

carteira_REITS['Valor'] = carteira_REITS.apply(lambda row: row.Qtd * row.Preço * row.USD, axis = 1)

total_acoesBR = round(carteira_acoesBR['Valor'].sum(),2)

total_FII = round(carteira_FII['Valor'].sum(),2)

total_acoesEUA = round(carteira_acoesEUA['Valor'].sum(),2)

total_REITS = round(carteira_REITS['Valor'].sum(),2)

total_Caixa = input('Insira o valor atual em caixa: ')
total_Caixa = float(total_Caixa)

total_carteira = total_acoesBR + total_FII + total_acoesEUA + total_REITS + total_Caixa

percentual_acoesBR = total_acoesBR / total_carteira
percentual_FII = total_FII / total_carteira
percentual_acoesEUA = total_acoesEUA / total_carteira
percentual_REITS = total_REITS / total_carteira
percentual_Caixa = total_Caixa / total_carteira

#definindo os percentuais ideais

carteira_acoesBR_ideal = carteira_ideal[carteira_ideal.Categoria=='Ações BR']
carteira_FII_ideal = carteira_ideal[carteira_ideal.Categoria=='FII']
carteira_acoesEUA_ideal = carteira_ideal[carteira_ideal.Categoria=='Ações EUA']
carteira_REITS_ideal = carteira_ideal[carteira_ideal.Categoria=='REIT EUA']
carteira_Caixa_ideal = carteira_ideal[carteira_ideal.Categoria=='Caixa']

ideal_acoesBR = carteira_acoesBR_ideal['Percentual'].tolist()
ideal_FII = carteira_FII_ideal['Percentual'].tolist()
ideal_acoesEUA = carteira_acoesEUA_ideal['Percentual'].tolist()
ideal_REITS = carteira_REITS_ideal['Percentual'].tolist()
ideal_Caixa = carteira_Caixa_ideal['Percentual'].tolist()


gap_percentual_acoes = percentual_acoesBR - ideal_acoesBR
gap_percentual_FII = percentual_FII - ideal_FII
gap_percentual_acoesEUA = percentual_acoesEUA - ideal_acoesEUA
gap_percentual_REITS = percentual_REITS - ideal_REITS
gap_percentual_Caixa = percentual_Caixa - ideal_Caixa

gap_percentual_acoes = round(float(gap_percentual_acoes),2) * 100
gap_percentual_FII = round(float(gap_percentual_FII),2) * 100
gap_percentual_REITS = round(float(gap_percentual_REITS),2) * 100
gap_percentual_acoesEUA = round(float(gap_percentual_acoesEUA),2) * 100
gap_percentual_Caixa = round(float(gap_percentual_Caixa),2) * 100

#Rebalanceamento por aporte

valor_aporte = input('Insira o valor do aporte: ')
valor_aporte = float(valor_aporte)

valor_total = valor_aporte + total_carteira

#Rebalanceamento Atual com aporte

percentual_acoesBR_aporte = total_acoesBR / valor_total
percentual_FII_aporte = total_FII / valor_total
percentual_acoesEUA_aporte = total_acoesEUA / valor_total
percentual_REITS_aporte = total_REITS / valor_total
percentual_Caixa_aporte = total_Caixa / valor_total
percentual_Aporte = valor_aporte / valor_total


carteira_pre_aporte = [total_acoesBR, total_FII, total_acoesEUA, total_REITS, total_Caixa, valor_aporte]
carteira = ['Ações BR', 'FII', 'Ações EUA', 'REITs', 'Caixa', 'Aporte']
carteira_perc_ideal = carteira_ideal['Percentual'].tolist()
carteira_perc_ideal.append(0)
carteira_perc_atual = [percentual_acoesBR_aporte, percentual_FII_aporte, percentual_acoesEUA_aporte, percentual_REITS_aporte, percentual_Caixa_aporte, percentual_Aporte]

carteira_balanceamento = pd.DataFrame(list(zip(carteira, carteira_pre_aporte, carteira_perc_atual,  carteira_perc_ideal)), columns=['Ativo', 'Valor', 'Perc_Atual', 'Perc_Ideal'])

#Calculo da diferença percentual entre atual vs ideal

carteira_balanceamento['Perc_Balanceamento'] = carteira_balanceamento.apply(lambda row: row.Perc_Ideal - row.Perc_Atual, axis = 1)

#Retirar casos que balanceamento < 0 e substituir por zero
carteira_balanceamento['Perc_Balanceamento'] = carteira_balanceamento['Perc_Balanceamento'].mask(carteira_balanceamento['Perc_Balanceamento'] < 0, 0)

Total_Perc_Balanceamento = carteira_balanceamento['Perc_Balanceamento'].sum()

carteira_balanceamento['Perc_Aporte'] = carteira_balanceamento.apply(lambda row: row.Perc_Balanceamento / Total_Perc_Balanceamento, axis = 1)

carteira_balanceamento['Valor_Aporte'] = carteira_balanceamento.apply(lambda row: row.Perc_Aporte * valor_aporte, axis = 1)

aportes = carteira_balanceamento['Valor_Aporte']

aporte_acoesBR = str(round(aportes[0],2))
aporte_FII = str(round(aportes[1],2))
aporte_acoesEUA = str(round(aportes[2],2))
aporte_REIT = str(round(aportes[3],2))
aporte_Caixa = str(round(aportes[4],2))
total_carteira = str(total_carteira)
total_Caixa = str(total_Caixa)
total_REITS = str(total_REITS)
total_acoesEUA = str(total_acoesEUA)
total_FII = str(total_FII)
total_acoesBR = str(total_acoesBR)
gap_percentual_acoes = str(gap_percentual_acoes)
gap_percentual_FII = str(gap_percentual_FII)
gap_percentual_REITS = str(gap_percentual_REITS)
gap_percentual_acoesEUA = str(gap_percentual_acoesEUA)
gap_percentual_Caixa = str(gap_percentual_Caixa)


print('\n\nVALOR TOTAL DA CARTEIRA  =  R$' + total_carteira + '\nValor em Ações BR = R$' + total_acoesBR + '\nValor em FIIs = R$' + total_FII + '\nValor em Ações EUA = R$' + total_acoesEUA + '\nValor em REITs = R$' + total_REITS + '\nValor em Caixa = R$' + total_Caixa)
      
print('\n\nDESBALANCEAMENTO:\nAções BR = '+ gap_percentual_acoes+'%'+'\nFIIs = '+ gap_percentual_FII+'%'+'\nAções EUA = '+ gap_percentual_acoesEUA+'%'+'\nREITs = '+ gap_percentual_REITS+'%'+'\nCaixa = '+ gap_percentual_Caixa+'%')

print('\n\nAPORTE:\nAções BR = R$'+ aporte_acoesBR+'\nFIIs = R$'+ aporte_FII+'\nAções EUA = R$'+ aporte_acoesEUA+'\nREITs = R$'+ aporte_REIT+'\nCaixa = R$'+ aporte_Caixa)
