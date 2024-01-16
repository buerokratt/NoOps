# check_dns.py
import dns.resolver
import dns.exception
import random  # Import the random module
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

def generate_funny_quote():
    quotes = [
        "Task did not fail successfuly!",
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "What's a computer's favorite beat? An algorithm!",
        "Why was the computer cold? It left its Windows open!",
        "How many programmers does it take to change a light bulb? None, that's a hardware issue!",
      
    ]
    return random.choice(quotes)

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
        box_width = 80  # Adjust the box width as needed
        main_domain_str = f" Main Domain: {main_domain} {'(exists)' if info['exists'] else '(does not exist)'}"
        main_domain_str = main_domain_str[:box_width - 2].center(box_width - 2)
        
        print(f"+{'=' * box_width}+")
        print(f"|{main_domain_str}|")
        print(f"+{'-' * box_width}+")

        for subdomain, subdomain_info in info["subdomains"].items():
            exists_str = "(exists)" if subdomain_info["exists"] else "(does not exist)"
            ips_str = ", ".join(subdomain_info["ips"]) if subdomain_info["ips"] else "No IPs found"
            
            subdomain_str = f" - Subdomain: {subdomain} {exists_str}"
            subdomain_str = subdomain_str[:box_width - 4].center(box_width - 4)
            
            ips_str = f"   IPs: {ips_str}"
            ips_str = ips_str[:box_width - 4].center(box_width - 4)

            print(f"|{subdomain_str}|")
            print(f"|{ips_str}|")

        print(f"+{'=' * box_width}+\n")

    # Generate and print a random funny quote
    print(generate_funny_quote())
