
SETTINGS:
START_NODES = [<node_0_1_i,4,i,0,4,1>]
END_NODES = [<node_5_2_i,4,i,0,4,1>]

START_POSITION = 0
END_POSITION = 0
START_VALUE = 0x8
END_VALUE = 0x8

DIFF_UP_BOUND = 128
LINEAR_UP_BOUND = 64
ENDSETTINGS

PARAMETERS:
s = [0x9,0x8,0x0,0x1,0xE,0xB,0xC,0xD,0x3,0x2,0x5,0x7,0xF,0xA,0x6,0x4]
ENDPARAMETERS

for r in range(0, 5)
{
    for j in range(0, 4)
    {
        SBOX(node_r_1_j, 4, node_r_2_j, 4, $s)

        DECOMPOSE(node_r_2_j, 4, 4, \
            node_r_3_(4*j),   1, \
            node_r_3_(4*j+1), 1, \
            node_r_3_(4*j+2), 1, \
            node_r_3_(4*j+3), 1)
    }

    for j in range(0, 4)
    {
        for k in range(0, 4)
        {
            EQ(node_r_3_(4*j+k), 1, node_r_4_(4*k+j), 1)
        }
    }

    for j in range(0, 4)
    {
        CASCADE(4, \
            node_r_4_(4*j),   1, \
            node_r_4_(4*j+1), 1, \
            node_r_4_(4*j+2), 1, \
            node_r_4_(4*j+3), 1, \
            node_(r+1)_1_j, 4)
    }
}

for j in range(0, 4)
{
    SBOX(node_5_1_j, 4, node_5_2_j, 4, $s)
}
