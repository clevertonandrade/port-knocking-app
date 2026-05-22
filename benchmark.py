import timeit
import validators

def bench_list(host):
    return any([validators.ipv4(host), validators.ipv6(host), validators.domain(host)])

def bench_or(host):
    return validators.ipv4(host) or validators.ipv6(host) or validators.domain(host)

hosts = ["127.0.0.1", "2001:0db8:85a3:0000:0000:8a2e:0370:7334", "example.com", "invalid-host"]

for host in hosts:
    print(f"Host: {host}")
    t_list = timeit.timeit(lambda: bench_list(host), number=10000)
    t_or = timeit.timeit(lambda: bench_or(host), number=10000)
    print(f"  List any: {t_list:.5f}s")
    print(f"  Or:       {t_or:.5f}s")
    print(f"  Improvement: {(t_list - t_or) / t_list * 100:.2f}%")
