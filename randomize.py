import random
import optparse

alphabet = [chr(i) for i in range(ord('A'),ord('Z')+1)]

def loss(s, vr, hr):
  s[vr][hr] = 'x'
  return s

def error(s, vr, hr):
  if s[vr][hr] != 'x':
    seqnum = s[vr][hr].split(',')[1]
    s[vr][hr] = random.choice(alphabet) + ',' + seqnum
  return s

def delay(s, vr, hr):
  if s[vr][hr] != 'x':
    i = hr + 1
    tmp1 = s[vr][hr]
    s[vr][hr] = 'x'
    while i < len(s[vr]):
      tmp2 = s[vr][i]
      s[vr][i] = tmp1
      tmp1 = tmp2
      i = i + 1 
    s[vr].append(tmp1)
  return s

parser = optparse.OptionParser()
parser.add_option("-i", "--input", action="store", type="string", dest="input",
                  help="input filename", metavar="INPUT")
parser.add_option("-o", "--output", action="store", type="string", dest="output",
                  help="output filename", metavar="OUTPUT")
parser.add_option("-l", "--losshor", action="store", type="float", dest="l_hor",
			 help="horizontal loss", metavar="LOSS HORIZONTAL")
parser.add_option("-r", "--loss_ver", action="store", type="float", dest="l_ver",
                help="vertical loss", metavar="LOSS VERTICAL")
parser.add_option("-e", "--error_hor", action="store", type="float", dest="e_hor",
                 help="horizontal error", metavar="ERROR HORIZONTAL")
parser.add_option("-a", "--error_ver", action="store", type="float", dest="e_ver",
                help="vertical error", metavar="ERROR VERTICAL")
parser.add_option("-d", "--delay_hor", action="store", type="float", dest="d_hor",
                 help="horizontal delay", metavar="ERROR HORIZONTAL")
parser.add_option("-g", "--delay_ver", action="store", type="float", dest="d_ver",
                help="vertical delay", metavar="DELAY VERTICAL")

(options, args) = parser.parse_args()

f = open(options.input, 'r')

s = []

avg_len = 0
for line in f:
  sibling_input = line.split()
  s.append(sibling_input)
  avg_len = avg_len + len(sibling_input)

avg_len = avg_len / len(s)

l_hor = options.l_hor
l_ver = options.l_ver

e_hor = options.e_hor
e_ver = options.e_ver

d_hor = options.d_hor
d_ver = options.d_ver

l_hor = int(l_hor * avg_len)
l_ver = int(l_ver * len(s))

loss_hor_rand =  random.sample(range(avg_len), l_hor)
loss_ver_rand =  random.sample(range(len(s)), l_ver)

e_hor = int(e_hor * avg_len)
e_ver = int(e_ver * len(s))

error_hor_rand =  random.sample(range(avg_len), e_hor)
error_ver_rand =  random.sample(range(len(s)), e_ver)

d_hor = int(d_hor * avg_len)
d_ver = int(d_ver * len(s))

delay_hor_rand =  random.sample(range(avg_len), d_hor)
delay_ver_rand =  random.sample(range(len(s)), d_ver)

for hr in loss_hor_rand:
  for vr in loss_ver_rand:
    s = loss(s, vr, hr)

for hr in error_hor_rand:
  for vr in error_ver_rand:
    s = error(s, vr, hr)

for hr in delay_hor_rand:
  for vr in delay_ver_rand:
    s = delay(s, vr, hr)

f = open(options.output, 'w')

for sibling_input in s:
  sibling_input = ' '.join(sibling_input)  
  f.write(sibling_input + '\n')
