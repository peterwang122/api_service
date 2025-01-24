import os
from typing import Dict, Any

# Redis 配置
REDIS_CONFIG: Dict[str, Any] = {
    "host": os.getenv("REDIS_HOST", "localhost"),  # Redis 主机地址
    "port": int(os.getenv("REDIS_PORT", 6379)),   # Redis 端口
    "db": int(os.getenv("REDIS_DB", 11)),          # Redis 数据库编号
    "password": os.getenv("REDIS_PASSWORD", None) # Redis 密码（可选）
}


CONFIG = {
    "OLD": {
        "AD": {
            "client_id": "amzn1.application-oa2-client.372e73f4a3364c21b6e91fc5e4fb09ba",
            "client_secret": "amzn1.oa2-cs.v1.a9e97a6bc4ffd44f6126f9184607da7add395f280ceff94fd400bf4352cb0df1"
        },
        "SP": {
            "client_id": "amzn1.application-oa2-client.79f5354080c64f5caa5f7455565bc327",
            "client_secret": "amzn1.oa2-cs.v1.9e9a47c17bb72fc1d73d3b4a4c41623cb3c9a4ae9b7ee59a76b5d563036877de"
        }
    },
    "NEW": {
        "AD": {
            "client_id": "amzn1.application-oa2-client.0b37f7cde8684cf8b96ddb1b6414ad8e",
            "client_secret": "amzn1.oa2-cs.v1.fb71b4650957525b85f953991d6615de143fc97fa755d91c121c7495fbbb68d4"
        },
        "SP": {
            "client_id": "amzn1.application-oa2-client.79f5354080c64f5caa5f7455565bc327",
            "client_secret": "amzn1.oa2-cs.v1.9e9a47c17bb72fc1d73d3b4a4c41623cb3c9a4ae9b7ee59a76b5d563036877de"
        }
    }
}
# config.py

CREDENTIALS = {
    "credentials": {
        "US": {
          "LAPASA":{
            "refresh_token": "Atzr|IwEBILZGTRCn9uaMRzOzYpHeypaLVhRVDqB4629lh2jB_FL19FXUBBu3CyzUvQ0eou8bec4HKZ7pqDButDAclWoKfyItkDOpzCq33AJybicXcj3y-7XUfHxbFoukrQZCGZDmmPGV5UlaNMcBP-l0B4nJi0hmomAwG5jgfi5ctJhmBwWvP2Al4inLTSYKsx1RW4CURflkJE51oRi1plwEvrjadN1d6rMKj0oGaRoJpaogcd-Md0U_cWXwOt4B5X9OdqtynKRGYDaXoBg4TvHe3qI0GfJjNgl9yF4lPHovV7t7n3dDnqUX7YYG7-B4pulzeA9S4tdfEF8Q9e1Rdztj8pZgor5sI4H3YUNnxCyOdZYtgxDh16FxQUyXMs1BAm2oQgajPKEhC1HpGbFJ3utnDiKbt1mxvwpuBAaF0D57ffWwVAxONHNJGRyFgJpwIl1ysyLALF6MycoxC3o8KphRFixhbPrp27CqKdogFusbIKZpVIx9yMQf7mmLqtEBdyYXq1xka9xcvunGCcH9bQn49hhZfmyxtA7qSDYbkd_7uqFdtPTF8tZ_kBhk3K4DEeoBHMix444xWAWNyqwDQHCMR4Ii_Gb5",
            "client_id": "amzn1.application-oa2-client.e06f4925f8ce481cad03749782631017",
            "client_secret": "2618b7d970591306ac73e2dc0d5341566cc2d5fd1b78eb33535b75f518cbf91b",
            "profile_id": "449424358596396"
              }
        },
        "UK": {
          "LAPASA":{
            "refresh_token": "Atzr|IwEBILZGTRCn9uaMRzOzYpHeypaLVhRVDqB4629lh2jB_FL19FXUBBu3CyzUvQ0eou8bec4HKZ7pqDButDAclWoKfyItkDOpzCq33AJybicXcj3y-7XUfHxbFoukrQZCGZDmmPGV5UlaNMcBP-l0B4nJi0hmomAwG5jgfi5ctJhmBwWvP2Al4inLTSYKsx1RW4CURflkJE51oRi1plwEvrjadN1d6rMKj0oGaRoJpaogcd-Md0U_cWXwOt4B5X9OdqtynKRGYDaXoBg4TvHe3qI0GfJjNgl9yF4lPHovV7t7n3dDnqUX7YYG7-B4pulzeA9S4tdfEF8Q9e1Rdztj8pZgor5sI4H3YUNnxCyOdZYtgxDh16FxQUyXMs1BAm2oQgajPKEhC1HpGbFJ3utnDiKbt1mxvwpuBAaF0D57ffWwVAxONHNJGRyFgJpwIl1ysyLALF6MycoxC3o8KphRFixhbPrp27CqKdogFusbIKZpVIx9yMQf7mmLqtEBdyYXq1xka9xcvunGCcH9bQn49hhZfmyxtA7qSDYbkd_7uqFdtPTF8tZ_kBhk3K4DEeoBHMix444xWAWNyqwDQHCMR4Ii_Gb5",
            "client_id": "amzn1.application-oa2-client.e06f4925f8ce481cad03749782631017",
            "client_secret": "2618b7d970591306ac73e2dc0d5341566cc2d5fd1b78eb33535b75f518cbf91b",
            "profile_id": "3129647433610131"
            },
          "DELOMO":{
            "refresh_token": "Atzr|IwEBIJqfuVdYGjPTII4TUp7OntbvXwH1nA7Yypl616w54GFz_NyJSwH91QRefiMh7oWXH6jO_Fd77o-fhzFzAP3ygUdQN24A7j0DTWNSCTTeSqlF3H3FyMoqunNuVZukZ78fRbV9B0apGHQoF82gfRcT37UGU_U1D_y-0F4DWiTRoB0S5nmo1ENxfiLC8oNIgddeL6eETk2pajOeAoOhCN9yaRIwWJKodktfBwjIJo45Tdw5dAb6_xuep3s9V1hmIGrkudmCCsma2EbEfGHxRGruBjgXsW4TGsskt-tUflGAgzGCld6vvIqLXUdq8fRp3NPYJDU5nnrzmMusyibLM1WbyRGElJhCyaQ1BpNAyd6ZWFSRxvx0M0GjI-5IpLaYAqnuoMRg7Nc-AGervbbhPlUVGrd7m_bSX3q_s8ndJuVa50mH8tvoii632xtyejPzXKj22qSoqRzGgu14HsdXItzY3ubo",
            "client_id": "amzn1.application-oa2-client.7e20eecc2d3747be94ea2bc27ee95ec8",
            "client_secret": "amzn1.oa2-cs.v1.1284058379fb0f5dfd55af49354282ad82041730729a7c8b4e0f817580b44bf4",
            "profile_id": "3841293982349425"
            },
          "OutdoorMaster":{
            "refresh_token": "Atzr|IwEBIPHqmU8N_w-2gVhMQdAP441V-V-U3G5tm889OlJBEY0IooS0lPB40jAK-mG3wN3ADqbn-OknxIjd1ACpg8hy-Qr17zaYNjHocSthlw_0ebr89C8VTHShS4aCsmzXavkRKG-UkRY0Tw4ODn-m21uXkbrDQKwAo48dWs--kbY2dB9xGveuOkeEEcjrBiRBVqZ5BAtByDaavPyfyjzqXq_Lc2-K5bf9B_I42uUmiU1cDA1m718m9ftcMAS4yrYZlcIFu82HGrXFTEpDfWgwKPbPHqOu0A50Yh4d-a-ikJRGve_8t47q8k5EsfaHP2xDJt0keyGxn5sj-BJE6JNNTPqah7QIx6bNcpvM2jRELTCgS4Kt8DBvKNTbYEY_9wmRQeKPsD-zs3FBwi-Va3Ni2d6CeP5XPBVvkbHwVAL2-I5et1EaZ5-J1EmRzSdLCy_GUVhFQ4t3sCmGa6nEDxY0Zb1AxVESepCgstfho6Mk2FYWCXwbj6wStiNxX811Z8mQRE2gNBv_Nd1J0A2cw5RBbQr0zwuX",
            "client_id": "amzn1.application-oa2-client.429e87002b214e6881eb8c85b385670d",
            "client_secret": "amzn1.oa2-cs.v1.1e4c5c7be9d622671e0fe23ac592c9baa7de151856d71b2f009acd3683da2e83",
            "profile_id": "1092878191220537"
            }
        },
        "DE": {
          "LAPASA":{
            "refresh_token": "Atzr|IwEBILZGTRCn9uaMRzOzYpHeypaLVhRVDqB4629lh2jB_FL19FXUBBu3CyzUvQ0eou8bec4HKZ7pqDButDAclWoKfyItkDOpzCq33AJybicXcj3y-7XUfHxbFoukrQZCGZDmmPGV5UlaNMcBP-l0B4nJi0hmomAwG5jgfi5ctJhmBwWvP2Al4inLTSYKsx1RW4CURflkJE51oRi1plwEvrjadN1d6rMKj0oGaRoJpaogcd-Md0U_cWXwOt4B5X9OdqtynKRGYDaXoBg4TvHe3qI0GfJjNgl9yF4lPHovV7t7n3dDnqUX7YYG7-B4pulzeA9S4tdfEF8Q9e1Rdztj8pZgor5sI4H3YUNnxCyOdZYtgxDh16FxQUyXMs1BAm2oQgajPKEhC1HpGbFJ3utnDiKbt1mxvwpuBAaF0D57ffWwVAxONHNJGRyFgJpwIl1ysyLALF6MycoxC3o8KphRFixhbPrp27CqKdogFusbIKZpVIx9yMQf7mmLqtEBdyYXq1xka9xcvunGCcH9bQn49hhZfmyxtA7qSDYbkd_7uqFdtPTF8tZ_kBhk3K4DEeoBHMix444xWAWNyqwDQHCMR4Ii_Gb5",
            "client_id": "amzn1.application-oa2-client.e06f4925f8ce481cad03749782631017",
            "client_secret": "2618b7d970591306ac73e2dc0d5341566cc2d5fd1b78eb33535b75f518cbf91b",
            "profile_id": "476439309435352"
          },
          "DELOMO":{
            "refresh_token": "Atzr|IwEBIJqfuVdYGjPTII4TUp7OntbvXwH1nA7Yypl616w54GFz_NyJSwH91QRefiMh7oWXH6jO_Fd77o-fhzFzAP3ygUdQN24A7j0DTWNSCTTeSqlF3H3FyMoqunNuVZukZ78fRbV9B0apGHQoF82gfRcT37UGU_U1D_y-0F4DWiTRoB0S5nmo1ENxfiLC8oNIgddeL6eETk2pajOeAoOhCN9yaRIwWJKodktfBwjIJo45Tdw5dAb6_xuep3s9V1hmIGrkudmCCsma2EbEfGHxRGruBjgXsW4TGsskt-tUflGAgzGCld6vvIqLXUdq8fRp3NPYJDU5nnrzmMusyibLM1WbyRGElJhCyaQ1BpNAyd6ZWFSRxvx0M0GjI-5IpLaYAqnuoMRg7Nc-AGervbbhPlUVGrd7m_bSX3q_s8ndJuVa50mH8tvoii632xtyejPzXKj22qSoqRzGgu14HsdXItzY3ubo",
            "client_id": "amzn1.application-oa2-client.7e20eecc2d3747be94ea2bc27ee95ec8",
            "client_secret": "amzn1.oa2-cs.v1.1284058379fb0f5dfd55af49354282ad82041730729a7c8b4e0f817580b44bf4",
            "profile_id": "1172377786256144"
            },
          "OutdoorMaster":{
            "refresh_token": "Atzr|IwEBIPHqmU8N_w-2gVhMQdAP441V-V-U3G5tm889OlJBEY0IooS0lPB40jAK-mG3wN3ADqbn-OknxIjd1ACpg8hy-Qr17zaYNjHocSthlw_0ebr89C8VTHShS4aCsmzXavkRKG-UkRY0Tw4ODn-m21uXkbrDQKwAo48dWs--kbY2dB9xGveuOkeEEcjrBiRBVqZ5BAtByDaavPyfyjzqXq_Lc2-K5bf9B_I42uUmiU1cDA1m718m9ftcMAS4yrYZlcIFu82HGrXFTEpDfWgwKPbPHqOu0A50Yh4d-a-ikJRGve_8t47q8k5EsfaHP2xDJt0keyGxn5sj-BJE6JNNTPqah7QIx6bNcpvM2jRELTCgS4Kt8DBvKNTbYEY_9wmRQeKPsD-zs3FBwi-Va3Ni2d6CeP5XPBVvkbHwVAL2-I5et1EaZ5-J1EmRzSdLCy_GUVhFQ4t3sCmGa6nEDxY0Zb1AxVESepCgstfho6Mk2FYWCXwbj6wStiNxX811Z8mQRE2gNBv_Nd1J0A2cw5RBbQr0zwuX",
            "client_id": "amzn1.application-oa2-client.429e87002b214e6881eb8c85b385670d",
            "client_secret": "amzn1.oa2-cs.v1.1e4c5c7be9d622671e0fe23ac592c9baa7de151856d71b2f009acd3683da2e83",
            "profile_id": "2341260822975712"
            }
        },
        "FR": {
          "LAPASA":{
            "refresh_token": "Atzr|IwEBILZGTRCn9uaMRzOzYpHeypaLVhRVDqB4629lh2jB_FL19FXUBBu3CyzUvQ0eou8bec4HKZ7pqDButDAclWoKfyItkDOpzCq33AJybicXcj3y-7XUfHxbFoukrQZCGZDmmPGV5UlaNMcBP-l0B4nJi0hmomAwG5jgfi5ctJhmBwWvP2Al4inLTSYKsx1RW4CURflkJE51oRi1plwEvrjadN1d6rMKj0oGaRoJpaogcd-Md0U_cWXwOt4B5X9OdqtynKRGYDaXoBg4TvHe3qI0GfJjNgl9yF4lPHovV7t7n3dDnqUX7YYG7-B4pulzeA9S4tdfEF8Q9e1Rdztj8pZgor5sI4H3YUNnxCyOdZYtgxDh16FxQUyXMs1BAm2oQgajPKEhC1HpGbFJ3utnDiKbt1mxvwpuBAaF0D57ffWwVAxONHNJGRyFgJpwIl1ysyLALF6MycoxC3o8KphRFixhbPrp27CqKdogFusbIKZpVIx9yMQf7mmLqtEBdyYXq1xka9xcvunGCcH9bQn49hhZfmyxtA7qSDYbkd_7uqFdtPTF8tZ_kBhk3K4DEeoBHMix444xWAWNyqwDQHCMR4Ii_Gb5",
            "client_id": "amzn1.application-oa2-client.e06f4925f8ce481cad03749782631017",
            "client_secret": "2618b7d970591306ac73e2dc0d5341566cc2d5fd1b78eb33535b75f518cbf91b",
            "profile_id": "3882496014426308"
          },
          "DELOMO":{
            "refresh_token": "Atzr|IwEBIJqfuVdYGjPTII4TUp7OntbvXwH1nA7Yypl616w54GFz_NyJSwH91QRefiMh7oWXH6jO_Fd77o-fhzFzAP3ygUdQN24A7j0DTWNSCTTeSqlF3H3FyMoqunNuVZukZ78fRbV9B0apGHQoF82gfRcT37UGU_U1D_y-0F4DWiTRoB0S5nmo1ENxfiLC8oNIgddeL6eETk2pajOeAoOhCN9yaRIwWJKodktfBwjIJo45Tdw5dAb6_xuep3s9V1hmIGrkudmCCsma2EbEfGHxRGruBjgXsW4TGsskt-tUflGAgzGCld6vvIqLXUdq8fRp3NPYJDU5nnrzmMusyibLM1WbyRGElJhCyaQ1BpNAyd6ZWFSRxvx0M0GjI-5IpLaYAqnuoMRg7Nc-AGervbbhPlUVGrd7m_bSX3q_s8ndJuVa50mH8tvoii632xtyejPzXKj22qSoqRzGgu14HsdXItzY3ubo",
            "client_id": "amzn1.application-oa2-client.7e20eecc2d3747be94ea2bc27ee95ec8",
            "client_secret": "amzn1.oa2-cs.v1.1284058379fb0f5dfd55af49354282ad82041730729a7c8b4e0f817580b44bf4",
            "profile_id": "1696832284279411"
            },
          "OutdoorMaster":{
            "refresh_token": "Atzr|IwEBIPHqmU8N_w-2gVhMQdAP441V-V-U3G5tm889OlJBEY0IooS0lPB40jAK-mG3wN3ADqbn-OknxIjd1ACpg8hy-Qr17zaYNjHocSthlw_0ebr89C8VTHShS4aCsmzXavkRKG-UkRY0Tw4ODn-m21uXkbrDQKwAo48dWs--kbY2dB9xGveuOkeEEcjrBiRBVqZ5BAtByDaavPyfyjzqXq_Lc2-K5bf9B_I42uUmiU1cDA1m718m9ftcMAS4yrYZlcIFu82HGrXFTEpDfWgwKPbPHqOu0A50Yh4d-a-ikJRGve_8t47q8k5EsfaHP2xDJt0keyGxn5sj-BJE6JNNTPqah7QIx6bNcpvM2jRELTCgS4Kt8DBvKNTbYEY_9wmRQeKPsD-zs3FBwi-Va3Ni2d6CeP5XPBVvkbHwVAL2-I5et1EaZ5-J1EmRzSdLCy_GUVhFQ4t3sCmGa6nEDxY0Zb1AxVESepCgstfho6Mk2FYWCXwbj6wStiNxX811Z8mQRE2gNBv_Nd1J0A2cw5RBbQr0zwuX",
            "client_id": "amzn1.application-oa2-client.429e87002b214e6881eb8c85b385670d",
            "client_secret": "amzn1.oa2-cs.v1.1e4c5c7be9d622671e0fe23ac592c9baa7de151856d71b2f009acd3683da2e83",
            "profile_id": "1684686676842788"
            }
        },
        "IT": {
          "LAPASA":{
            "refresh_token": "Atzr|IwEBILZGTRCn9uaMRzOzYpHeypaLVhRVDqB4629lh2jB_FL19FXUBBu3CyzUvQ0eou8bec4HKZ7pqDButDAclWoKfyItkDOpzCq33AJybicXcj3y-7XUfHxbFoukrQZCGZDmmPGV5UlaNMcBP-l0B4nJi0hmomAwG5jgfi5ctJhmBwWvP2Al4inLTSYKsx1RW4CURflkJE51oRi1plwEvrjadN1d6rMKj0oGaRoJpaogcd-Md0U_cWXwOt4B5X9OdqtynKRGYDaXoBg4TvHe3qI0GfJjNgl9yF4lPHovV7t7n3dDnqUX7YYG7-B4pulzeA9S4tdfEF8Q9e1Rdztj8pZgor5sI4H3YUNnxCyOdZYtgxDh16FxQUyXMs1BAm2oQgajPKEhC1HpGbFJ3utnDiKbt1mxvwpuBAaF0D57ffWwVAxONHNJGRyFgJpwIl1ysyLALF6MycoxC3o8KphRFixhbPrp27CqKdogFusbIKZpVIx9yMQf7mmLqtEBdyYXq1xka9xcvunGCcH9bQn49hhZfmyxtA7qSDYbkd_7uqFdtPTF8tZ_kBhk3K4DEeoBHMix444xWAWNyqwDQHCMR4Ii_Gb5",
            "client_id": "amzn1.application-oa2-client.e06f4925f8ce481cad03749782631017",
            "client_secret": "2618b7d970591306ac73e2dc0d5341566cc2d5fd1b78eb33535b75f518cbf91b",
            "profile_id": "4390773876358927"
          },
          "DELOMO":{
            "refresh_token": "Atzr|IwEBIJqfuVdYGjPTII4TUp7OntbvXwH1nA7Yypl616w54GFz_NyJSwH91QRefiMh7oWXH6jO_Fd77o-fhzFzAP3ygUdQN24A7j0DTWNSCTTeSqlF3H3FyMoqunNuVZukZ78fRbV9B0apGHQoF82gfRcT37UGU_U1D_y-0F4DWiTRoB0S5nmo1ENxfiLC8oNIgddeL6eETk2pajOeAoOhCN9yaRIwWJKodktfBwjIJo45Tdw5dAb6_xuep3s9V1hmIGrkudmCCsma2EbEfGHxRGruBjgXsW4TGsskt-tUflGAgzGCld6vvIqLXUdq8fRp3NPYJDU5nnrzmMusyibLM1WbyRGElJhCyaQ1BpNAyd6ZWFSRxvx0M0GjI-5IpLaYAqnuoMRg7Nc-AGervbbhPlUVGrd7m_bSX3q_s8ndJuVa50mH8tvoii632xtyejPzXKj22qSoqRzGgu14HsdXItzY3ubo",
            "client_id": "amzn1.application-oa2-client.7e20eecc2d3747be94ea2bc27ee95ec8",
            "client_secret": "amzn1.oa2-cs.v1.1284058379fb0f5dfd55af49354282ad82041730729a7c8b4e0f817580b44bf4",
            "profile_id": "1070926604434581"
            },
          "OutdoorMaster":{
            "refresh_token": "Atzr|IwEBIPHqmU8N_w-2gVhMQdAP441V-V-U3G5tm889OlJBEY0IooS0lPB40jAK-mG3wN3ADqbn-OknxIjd1ACpg8hy-Qr17zaYNjHocSthlw_0ebr89C8VTHShS4aCsmzXavkRKG-UkRY0Tw4ODn-m21uXkbrDQKwAo48dWs--kbY2dB9xGveuOkeEEcjrBiRBVqZ5BAtByDaavPyfyjzqXq_Lc2-K5bf9B_I42uUmiU1cDA1m718m9ftcMAS4yrYZlcIFu82HGrXFTEpDfWgwKPbPHqOu0A50Yh4d-a-ikJRGve_8t47q8k5EsfaHP2xDJt0keyGxn5sj-BJE6JNNTPqah7QIx6bNcpvM2jRELTCgS4Kt8DBvKNTbYEY_9wmRQeKPsD-zs3FBwi-Va3Ni2d6CeP5XPBVvkbHwVAL2-I5et1EaZ5-J1EmRzSdLCy_GUVhFQ4t3sCmGa6nEDxY0Zb1AxVESepCgstfho6Mk2FYWCXwbj6wStiNxX811Z8mQRE2gNBv_Nd1J0A2cw5RBbQr0zwuX",
            "client_id": "amzn1.application-oa2-client.429e87002b214e6881eb8c85b385670d",
            "client_secret": "amzn1.oa2-cs.v1.1e4c5c7be9d622671e0fe23ac592c9baa7de151856d71b2f009acd3683da2e83",
            "profile_id": "3927518530959614"
            }
        },
        "ES": {
          "LAPASA":{
            "refresh_token": "Atzr|IwEBILZGTRCn9uaMRzOzYpHeypaLVhRVDqB4629lh2jB_FL19FXUBBu3CyzUvQ0eou8bec4HKZ7pqDButDAclWoKfyItkDOpzCq33AJybicXcj3y-7XUfHxbFoukrQZCGZDmmPGV5UlaNMcBP-l0B4nJi0hmomAwG5jgfi5ctJhmBwWvP2Al4inLTSYKsx1RW4CURflkJE51oRi1plwEvrjadN1d6rMKj0oGaRoJpaogcd-Md0U_cWXwOt4B5X9OdqtynKRGYDaXoBg4TvHe3qI0GfJjNgl9yF4lPHovV7t7n3dDnqUX7YYG7-B4pulzeA9S4tdfEF8Q9e1Rdztj8pZgor5sI4H3YUNnxCyOdZYtgxDh16FxQUyXMs1BAm2oQgajPKEhC1HpGbFJ3utnDiKbt1mxvwpuBAaF0D57ffWwVAxONHNJGRyFgJpwIl1ysyLALF6MycoxC3o8KphRFixhbPrp27CqKdogFusbIKZpVIx9yMQf7mmLqtEBdyYXq1xka9xcvunGCcH9bQn49hhZfmyxtA7qSDYbkd_7uqFdtPTF8tZ_kBhk3K4DEeoBHMix444xWAWNyqwDQHCMR4Ii_Gb5",
            "client_id": "amzn1.application-oa2-client.e06f4925f8ce481cad03749782631017",
            "client_secret": "2618b7d970591306ac73e2dc0d5341566cc2d5fd1b78eb33535b75f518cbf91b",
            "profile_id": "2877849784870332"
          },
          "DELOMO":{
            "refresh_token": "Atzr|IwEBIJqfuVdYGjPTII4TUp7OntbvXwH1nA7Yypl616w54GFz_NyJSwH91QRefiMh7oWXH6jO_Fd77o-fhzFzAP3ygUdQN24A7j0DTWNSCTTeSqlF3H3FyMoqunNuVZukZ78fRbV9B0apGHQoF82gfRcT37UGU_U1D_y-0F4DWiTRoB0S5nmo1ENxfiLC8oNIgddeL6eETk2pajOeAoOhCN9yaRIwWJKodktfBwjIJo45Tdw5dAb6_xuep3s9V1hmIGrkudmCCsma2EbEfGHxRGruBjgXsW4TGsskt-tUflGAgzGCld6vvIqLXUdq8fRp3NPYJDU5nnrzmMusyibLM1WbyRGElJhCyaQ1BpNAyd6ZWFSRxvx0M0GjI-5IpLaYAqnuoMRg7Nc-AGervbbhPlUVGrd7m_bSX3q_s8ndJuVa50mH8tvoii632xtyejPzXKj22qSoqRzGgu14HsdXItzY3ubo",
            "client_id": "amzn1.application-oa2-client.7e20eecc2d3747be94ea2bc27ee95ec8",
            "client_secret": "amzn1.oa2-cs.v1.1284058379fb0f5dfd55af49354282ad82041730729a7c8b4e0f817580b44bf4",
            "profile_id": "435929316382615"
            },
          "OutdoorMaster":{
            "refresh_token": "Atzr|IwEBIPHqmU8N_w-2gVhMQdAP441V-V-U3G5tm889OlJBEY0IooS0lPB40jAK-mG3wN3ADqbn-OknxIjd1ACpg8hy-Qr17zaYNjHocSthlw_0ebr89C8VTHShS4aCsmzXavkRKG-UkRY0Tw4ODn-m21uXkbrDQKwAo48dWs--kbY2dB9xGveuOkeEEcjrBiRBVqZ5BAtByDaavPyfyjzqXq_Lc2-K5bf9B_I42uUmiU1cDA1m718m9ftcMAS4yrYZlcIFu82HGrXFTEpDfWgwKPbPHqOu0A50Yh4d-a-ikJRGve_8t47q8k5EsfaHP2xDJt0keyGxn5sj-BJE6JNNTPqah7QIx6bNcpvM2jRELTCgS4Kt8DBvKNTbYEY_9wmRQeKPsD-zs3FBwi-Va3Ni2d6CeP5XPBVvkbHwVAL2-I5et1EaZ5-J1EmRzSdLCy_GUVhFQ4t3sCmGa6nEDxY0Zb1AxVESepCgstfho6Mk2FYWCXwbj6wStiNxX811Z8mQRE2gNBv_Nd1J0A2cw5RBbQr0zwuX",
            "client_id": "amzn1.application-oa2-client.429e87002b214e6881eb8c85b385670d",
            "client_secret": "amzn1.oa2-cs.v1.1e4c5c7be9d622671e0fe23ac592c9baa7de151856d71b2f009acd3683da2e83",
            "profile_id": "805792909678917"
            }
        },
        "NL": {
          "LAPASA":{
            "refresh_token": "Atzr|IwEBILZGTRCn9uaMRzOzYpHeypaLVhRVDqB4629lh2jB_FL19FXUBBu3CyzUvQ0eou8bec4HKZ7pqDButDAclWoKfyItkDOpzCq33AJybicXcj3y-7XUfHxbFoukrQZCGZDmmPGV5UlaNMcBP-l0B4nJi0hmomAwG5jgfi5ctJhmBwWvP2Al4inLTSYKsx1RW4CURflkJE51oRi1plwEvrjadN1d6rMKj0oGaRoJpaogcd-Md0U_cWXwOt4B5X9OdqtynKRGYDaXoBg4TvHe3qI0GfJjNgl9yF4lPHovV7t7n3dDnqUX7YYG7-B4pulzeA9S4tdfEF8Q9e1Rdztj8pZgor5sI4H3YUNnxCyOdZYtgxDh16FxQUyXMs1BAm2oQgajPKEhC1HpGbFJ3utnDiKbt1mxvwpuBAaF0D57ffWwVAxONHNJGRyFgJpwIl1ysyLALF6MycoxC3o8KphRFixhbPrp27CqKdogFusbIKZpVIx9yMQf7mmLqtEBdyYXq1xka9xcvunGCcH9bQn49hhZfmyxtA7qSDYbkd_7uqFdtPTF8tZ_kBhk3K4DEeoBHMix444xWAWNyqwDQHCMR4Ii_Gb5",
            "client_id": "amzn1.application-oa2-client.e06f4925f8ce481cad03749782631017",
            "client_secret": "2618b7d970591306ac73e2dc0d5341566cc2d5fd1b78eb33535b75f518cbf91b",
            "profile_id": "2345553321664655"
          },
          "OutdoorMaster":{
            "refresh_token": "Atzr|IwEBIPHqmU8N_w-2gVhMQdAP441V-V-U3G5tm889OlJBEY0IooS0lPB40jAK-mG3wN3ADqbn-OknxIjd1ACpg8hy-Qr17zaYNjHocSthlw_0ebr89C8VTHShS4aCsmzXavkRKG-UkRY0Tw4ODn-m21uXkbrDQKwAo48dWs--kbY2dB9xGveuOkeEEcjrBiRBVqZ5BAtByDaavPyfyjzqXq_Lc2-K5bf9B_I42uUmiU1cDA1m718m9ftcMAS4yrYZlcIFu82HGrXFTEpDfWgwKPbPHqOu0A50Yh4d-a-ikJRGve_8t47q8k5EsfaHP2xDJt0keyGxn5sj-BJE6JNNTPqah7QIx6bNcpvM2jRELTCgS4Kt8DBvKNTbYEY_9wmRQeKPsD-zs3FBwi-Va3Ni2d6CeP5XPBVvkbHwVAL2-I5et1EaZ5-J1EmRzSdLCy_GUVhFQ4t3sCmGa6nEDxY0Zb1AxVESepCgstfho6Mk2FYWCXwbj6wStiNxX811Z8mQRE2gNBv_Nd1J0A2cw5RBbQr0zwuX",
            "client_id": "amzn1.application-oa2-client.429e87002b214e6881eb8c85b385670d",
            "client_secret": "amzn1.oa2-cs.v1.1e4c5c7be9d622671e0fe23ac592c9baa7de151856d71b2f009acd3683da2e83",
            "profile_id": "1664278096574440"
            }
        },
        "SE": {
          "LAPASA":{
            "refresh_token": "Atzr|IwEBILZGTRCn9uaMRzOzYpHeypaLVhRVDqB4629lh2jB_FL19FXUBBu3CyzUvQ0eou8bec4HKZ7pqDButDAclWoKfyItkDOpzCq33AJybicXcj3y-7XUfHxbFoukrQZCGZDmmPGV5UlaNMcBP-l0B4nJi0hmomAwG5jgfi5ctJhmBwWvP2Al4inLTSYKsx1RW4CURflkJE51oRi1plwEvrjadN1d6rMKj0oGaRoJpaogcd-Md0U_cWXwOt4B5X9OdqtynKRGYDaXoBg4TvHe3qI0GfJjNgl9yF4lPHovV7t7n3dDnqUX7YYG7-B4pulzeA9S4tdfEF8Q9e1Rdztj8pZgor5sI4H3YUNnxCyOdZYtgxDh16FxQUyXMs1BAm2oQgajPKEhC1HpGbFJ3utnDiKbt1mxvwpuBAaF0D57ffWwVAxONHNJGRyFgJpwIl1ysyLALF6MycoxC3o8KphRFixhbPrp27CqKdogFusbIKZpVIx9yMQf7mmLqtEBdyYXq1xka9xcvunGCcH9bQn49hhZfmyxtA7qSDYbkd_7uqFdtPTF8tZ_kBhk3K4DEeoBHMix444xWAWNyqwDQHCMR4Ii_Gb5",
            "client_id": "amzn1.application-oa2-client.e06f4925f8ce481cad03749782631017",
            "client_secret": "2618b7d970591306ac73e2dc0d5341566cc2d5fd1b78eb33535b75f518cbf91b",
            "profile_id": "2017587388563369"
          },
          "OutdoorMaster":{
            "refresh_token": "Atzr|IwEBIPHqmU8N_w-2gVhMQdAP441V-V-U3G5tm889OlJBEY0IooS0lPB40jAK-mG3wN3ADqbn-OknxIjd1ACpg8hy-Qr17zaYNjHocSthlw_0ebr89C8VTHShS4aCsmzXavkRKG-UkRY0Tw4ODn-m21uXkbrDQKwAo48dWs--kbY2dB9xGveuOkeEEcjrBiRBVqZ5BAtByDaavPyfyjzqXq_Lc2-K5bf9B_I42uUmiU1cDA1m718m9ftcMAS4yrYZlcIFu82HGrXFTEpDfWgwKPbPHqOu0A50Yh4d-a-ikJRGve_8t47q8k5EsfaHP2xDJt0keyGxn5sj-BJE6JNNTPqah7QIx6bNcpvM2jRELTCgS4Kt8DBvKNTbYEY_9wmRQeKPsD-zs3FBwi-Va3Ni2d6CeP5XPBVvkbHwVAL2-I5et1EaZ5-J1EmRzSdLCy_GUVhFQ4t3sCmGa6nEDxY0Zb1AxVESepCgstfho6Mk2FYWCXwbj6wStiNxX811Z8mQRE2gNBv_Nd1J0A2cw5RBbQr0zwuX",
            "client_id": "amzn1.application-oa2-client.429e87002b214e6881eb8c85b385670d",
            "client_secret": "amzn1.oa2-cs.v1.1e4c5c7be9d622671e0fe23ac592c9baa7de151856d71b2f009acd3683da2e83",
            "profile_id": "3141634691424470"
            }
        },
        "PL": {
          "LAPASA":{
            "refresh_token": "Atzr|IwEBILZGTRCn9uaMRzOzYpHeypaLVhRVDqB4629lh2jB_FL19FXUBBu3CyzUvQ0eou8bec4HKZ7pqDButDAclWoKfyItkDOpzCq33AJybicXcj3y-7XUfHxbFoukrQZCGZDmmPGV5UlaNMcBP-l0B4nJi0hmomAwG5jgfi5ctJhmBwWvP2Al4inLTSYKsx1RW4CURflkJE51oRi1plwEvrjadN1d6rMKj0oGaRoJpaogcd-Md0U_cWXwOt4B5X9OdqtynKRGYDaXoBg4TvHe3qI0GfJjNgl9yF4lPHovV7t7n3dDnqUX7YYG7-B4pulzeA9S4tdfEF8Q9e1Rdztj8pZgor5sI4H3YUNnxCyOdZYtgxDh16FxQUyXMs1BAm2oQgajPKEhC1HpGbFJ3utnDiKbt1mxvwpuBAaF0D57ffWwVAxONHNJGRyFgJpwIl1ysyLALF6MycoxC3o8KphRFixhbPrp27CqKdogFusbIKZpVIx9yMQf7mmLqtEBdyYXq1xka9xcvunGCcH9bQn49hhZfmyxtA7qSDYbkd_7uqFdtPTF8tZ_kBhk3K4DEeoBHMix444xWAWNyqwDQHCMR4Ii_Gb5",
            "client_id": "amzn1.application-oa2-client.e06f4925f8ce481cad03749782631017",
            "client_secret": "2618b7d970591306ac73e2dc0d5341566cc2d5fd1b78eb33535b75f518cbf91b",
            "profile_id": "2897727332905398"
          },
          "OutdoorMaster":{
            "refresh_token": "Atzr|IwEBIPHqmU8N_w-2gVhMQdAP441V-V-U3G5tm889OlJBEY0IooS0lPB40jAK-mG3wN3ADqbn-OknxIjd1ACpg8hy-Qr17zaYNjHocSthlw_0ebr89C8VTHShS4aCsmzXavkRKG-UkRY0Tw4ODn-m21uXkbrDQKwAo48dWs--kbY2dB9xGveuOkeEEcjrBiRBVqZ5BAtByDaavPyfyjzqXq_Lc2-K5bf9B_I42uUmiU1cDA1m718m9ftcMAS4yrYZlcIFu82HGrXFTEpDfWgwKPbPHqOu0A50Yh4d-a-ikJRGve_8t47q8k5EsfaHP2xDJt0keyGxn5sj-BJE6JNNTPqah7QIx6bNcpvM2jRELTCgS4Kt8DBvKNTbYEY_9wmRQeKPsD-zs3FBwi-Va3Ni2d6CeP5XPBVvkbHwVAL2-I5et1EaZ5-J1EmRzSdLCy_GUVhFQ4t3sCmGa6nEDxY0Zb1AxVESepCgstfho6Mk2FYWCXwbj6wStiNxX811Z8mQRE2gNBv_Nd1J0A2cw5RBbQr0zwuX",
            "client_id": "amzn1.application-oa2-client.429e87002b214e6881eb8c85b385670d",
            "client_secret": "amzn1.oa2-cs.v1.1e4c5c7be9d622671e0fe23ac592c9baa7de151856d71b2f009acd3683da2e83",
            "profile_id": "2336672588905088"
            }
        },
        "TR": {
          "LAPASA":{
            "refresh_token": "Atzr|IwEBILZGTRCn9uaMRzOzYpHeypaLVhRVDqB4629lh2jB_FL19FXUBBu3CyzUvQ0eou8bec4HKZ7pqDButDAclWoKfyItkDOpzCq33AJybicXcj3y-7XUfHxbFoukrQZCGZDmmPGV5UlaNMcBP-l0B4nJi0hmomAwG5jgfi5ctJhmBwWvP2Al4inLTSYKsx1RW4CURflkJE51oRi1plwEvrjadN1d6rMKj0oGaRoJpaogcd-Md0U_cWXwOt4B5X9OdqtynKRGYDaXoBg4TvHe3qI0GfJjNgl9yF4lPHovV7t7n3dDnqUX7YYG7-B4pulzeA9S4tdfEF8Q9e1Rdztj8pZgor5sI4H3YUNnxCyOdZYtgxDh16FxQUyXMs1BAm2oQgajPKEhC1HpGbFJ3utnDiKbt1mxvwpuBAaF0D57ffWwVAxONHNJGRyFgJpwIl1ysyLALF6MycoxC3o8KphRFixhbPrp27CqKdogFusbIKZpVIx9yMQf7mmLqtEBdyYXq1xka9xcvunGCcH9bQn49hhZfmyxtA7qSDYbkd_7uqFdtPTF8tZ_kBhk3K4DEeoBHMix444xWAWNyqwDQHCMR4Ii_Gb5",
            "client_id": "amzn1.application-oa2-client.e06f4925f8ce481cad03749782631017",
            "client_secret": "2618b7d970591306ac73e2dc0d5341566cc2d5fd1b78eb33535b75f518cbf91b",
            "profile_id": "2371860816858625"
          },
          "OutdoorMaster":{
            "refresh_token": "Atzr|IwEBIPHqmU8N_w-2gVhMQdAP441V-V-U3G5tm889OlJBEY0IooS0lPB40jAK-mG3wN3ADqbn-OknxIjd1ACpg8hy-Qr17zaYNjHocSthlw_0ebr89C8VTHShS4aCsmzXavkRKG-UkRY0Tw4ODn-m21uXkbrDQKwAo48dWs--kbY2dB9xGveuOkeEEcjrBiRBVqZ5BAtByDaavPyfyjzqXq_Lc2-K5bf9B_I42uUmiU1cDA1m718m9ftcMAS4yrYZlcIFu82HGrXFTEpDfWgwKPbPHqOu0A50Yh4d-a-ikJRGve_8t47q8k5EsfaHP2xDJt0keyGxn5sj-BJE6JNNTPqah7QIx6bNcpvM2jRELTCgS4Kt8DBvKNTbYEY_9wmRQeKPsD-zs3FBwi-Va3Ni2d6CeP5XPBVvkbHwVAL2-I5et1EaZ5-J1EmRzSdLCy_GUVhFQ4t3sCmGa6nEDxY0Zb1AxVESepCgstfho6Mk2FYWCXwbj6wStiNxX811Z8mQRE2gNBv_Nd1J0A2cw5RBbQr0zwuX",
            "client_id": "amzn1.application-oa2-client.429e87002b214e6881eb8c85b385670d",
            "client_secret": "amzn1.oa2-cs.v1.1e4c5c7be9d622671e0fe23ac592c9baa7de151856d71b2f009acd3683da2e83",
            "profile_id": "1289987588549772"
            }
        },
        "BE": {
          "LAPASA":{
            "refresh_token": "Atzr|IwEBILZGTRCn9uaMRzOzYpHeypaLVhRVDqB4629lh2jB_FL19FXUBBu3CyzUvQ0eou8bec4HKZ7pqDButDAclWoKfyItkDOpzCq33AJybicXcj3y-7XUfHxbFoukrQZCGZDmmPGV5UlaNMcBP-l0B4nJi0hmomAwG5jgfi5ctJhmBwWvP2Al4inLTSYKsx1RW4CURflkJE51oRi1plwEvrjadN1d6rMKj0oGaRoJpaogcd-Md0U_cWXwOt4B5X9OdqtynKRGYDaXoBg4TvHe3qI0GfJjNgl9yF4lPHovV7t7n3dDnqUX7YYG7-B4pulzeA9S4tdfEF8Q9e1Rdztj8pZgor5sI4H3YUNnxCyOdZYtgxDh16FxQUyXMs1BAm2oQgajPKEhC1HpGbFJ3utnDiKbt1mxvwpuBAaF0D57ffWwVAxONHNJGRyFgJpwIl1ysyLALF6MycoxC3o8KphRFixhbPrp27CqKdogFusbIKZpVIx9yMQf7mmLqtEBdyYXq1xka9xcvunGCcH9bQn49hhZfmyxtA7qSDYbkd_7uqFdtPTF8tZ_kBhk3K4DEeoBHMix444xWAWNyqwDQHCMR4Ii_Gb5",
            "client_id": "amzn1.application-oa2-client.e06f4925f8ce481cad03749782631017",
            "client_secret": "2618b7d970591306ac73e2dc0d5341566cc2d5fd1b78eb33535b75f518cbf91b",
            "profile_id": "4275789292164320"
          }
        },
        "JP": {
            "LAPASA":{
              "refresh_token": "Atzr|IwEBILZGTRCn9uaMRzOzYpHeypaLVhRVDqB4629lh2jB_FL19FXUBBu3CyzUvQ0eou8bec4HKZ7pqDButDAclWoKfyItkDOpzCq33AJybicXcj3y-7XUfHxbFoukrQZCGZDmmPGV5UlaNMcBP-l0B4nJi0hmomAwG5jgfi5ctJhmBwWvP2Al4inLTSYKsx1RW4CURflkJE51oRi1plwEvrjadN1d6rMKj0oGaRoJpaogcd-Md0U_cWXwOt4B5X9OdqtynKRGYDaXoBg4TvHe3qI0GfJjNgl9yF4lPHovV7t7n3dDnqUX7YYG7-B4pulzeA9S4tdfEF8Q9e1Rdztj8pZgor5sI4H3YUNnxCyOdZYtgxDh16FxQUyXMs1BAm2oQgajPKEhC1HpGbFJ3utnDiKbt1mxvwpuBAaF0D57ffWwVAxONHNJGRyFgJpwIl1ysyLALF6MycoxC3o8KphRFixhbPrp27CqKdogFusbIKZpVIx9yMQf7mmLqtEBdyYXq1xka9xcvunGCcH9bQn49hhZfmyxtA7qSDYbkd_7uqFdtPTF8tZ_kBhk3K4DEeoBHMix444xWAWNyqwDQHCMR4Ii_Gb5",
              "client_id": "amzn1.application-oa2-client.e06f4925f8ce481cad03749782631017",
              "client_secret": "2618b7d970591306ac73e2dc0d5341566cc2d5fd1b78eb33535b75f518cbf91b",
              "profile_id": "2275352415590999"
            }
          }
    }
}

# config.py

COUNTRY_REGION_MAPPING = {
    "US": "NA",
    "CA": "NA",
    "MX": "NA",
    "BR": "NA",
    "JP": "FE",
    "AU": "FE",
    "SG": "FE",
    "ES": "EU",
    "DE": "EU",
    "FR": "EU",
    "IT": "EU",
    "NL": "EU",
    "BE": "EU",
    "UK": "EU",
    "AE": "EU",
    "SE": "EU",
    "PL": "EU",
    "TR": "EU",
    "IN": "EU",
    "SA": "EU",
    "EG": "EU"
}
# # 其他项目配置
# OTHER_CONFIG: Dict[str, Any] = {
#     "max_retries": 3,  # 最大重试次数
#     "timeout": 10      # 超时时间（秒）
# }