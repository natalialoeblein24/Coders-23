#!/usr/bin/env python
# coding: utf-8

# In[5]:


idade = int(input('idade: '))


# In[6]:


type(idade)


# In[7]:


str(float(idade))


# In[9]:


int('00123') # para comentar mais linha """3 aspas"""


# In[16]:


print('podemos pular \\n linhas se quisermos') #usando duas \\ ele lê como string o \n


# In[ ]:


print # tab para auto-complete


# In[19]:


print('""') #teste


# In[20]:


"text" #no jupyter a ultima linha da celula funciona parecido com o print - coloca o texto como aspas simples


# In[23]:


print('texto2')
'texto1'


# In[25]:


print('podemos usar "end" para finalizar, é util em condicinoais' , end='.')


# In[34]:


nome = input('Insira seu nome: ')
sobrenome = input('insira seu sobrenome: ')
idade = int(input('Insira sua idade: '))
hobby = input('Insira seu hobby: ')

# print('Olá,', nome , sobrenome , 'você tem', idade, 'anos', end='.' )

print(f'Olá, eu sou {nome} {sobrenome} e tenho {idade} anos e meu hobby é {hobby}', end='.') # usando f (f string) na frente


# In[30]:


print('Olá, eu sou {nome} {sobrenome} e tenho {idade} anos')


# In[39]:


name = input("Enter your name: ")
age = float(input("Enter your age: "))
hobby = input("What's your hobby? ")

print(f"Hey, {name}, good to know that you have {age} years and your hobby is {hobby}")


# In[ ]:




