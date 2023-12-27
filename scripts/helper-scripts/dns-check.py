# check_dns.py
import dns.resolver
import dns.exception
from dns_config import dns_names, main_domains

def extract_main_domain(full_domain):
    parts = full_domain.split('.')
    return '.'.join(parts[-2:])  # Return the last two parts of the domain

def get_domain_info(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        ips = [answer.address for answer in result]
        return {"ips": ips, "exists": True}
    except dns.resolver.NXDOMAIN:
        return {"ips": [], "exists": False}
    except dns.exception.DNSException:
        return {"ips": [], "exists": False}

if __name__ == "__main__":
    domain_dict = {}

    for main_domain in main_domains:
        domain_dict[main_domain] = {"subdomains": {}, "exists": None}

        for domain in dns_names:
            if domain.endswith(f".{main_domain}"):
                main_domain_info = get_domain_info(main_domain)
                subdomain_info = get_domain_info(domain)

                domain_dict[main_domain]["exists"] = main_domain_info["exists"]
                domain_dict[main_domain]["subdomains"][domain] = {
                    "exists": subdomain_info["exists"],
                    "ips": subdomain_info["ips"]
                }

    # Print the results
    for main_domain, info in domain_dict.items():
        print(f"Main Domain: {main_domain} {'(exists)' if info['exists'] else '(does not exist)'}")

        for subdomain, subdomain_info in info["subdomains"].items():
            exists_str = "(exists)" if subdomain_info["exists"] else "(does not exist)"
            ips_str = ", ".join(subdomain_info["ips"]) if subdomain_info["ips"] else "No IPs found"
            print(f"  - Subdomain: {subdomain} {exists_str}")
            print(f"    IPs: {ips_str}")

    print("\nScript finished.")
