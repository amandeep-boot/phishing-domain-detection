"""
Full Feature Extractor for GregaVrbancic Dataset (111 features)
Matches the features used in training the Deep Learning model
"""

import re
from urllib.parse import urlparse, parse_qs
import tldextract

class FullFeatureExtractor:
    """Extract all 111 features from URLs for phishing detection"""
    
    def extract_features(self, url):
        """
        Extract all 111 features from a URL
        Returns a dictionary with feature names as keys
        """
        # Ensure URL has a scheme
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        # Parse URL
        parsed = urlparse(url)
        extracted = tldextract.extract(url)
        
        # Split URL into components
        domain = f"{extracted.domain}.{extracted.suffix}" if extracted.suffix else extracted.domain
        directory = parsed.path.split('?')[0] if '?' in parsed.path else parsed.path
        file_part = directory.split('/')[-1] if '/' in directory else ''
        params = parsed.query
        
        features = {}
        
        # URL features (17 features)
        features['qty_dot_url'] = url.count('.')
        features['qty_hyphen_url'] = url.count('-')
        features['qty_underline_url'] = url.count('_')
        features['qty_slash_url'] = url.count('/')
        features['qty_questionmark_url'] = url.count('?')
        features['qty_equal_url'] = url.count('=')
        features['qty_at_url'] = url.count('@')
        features['qty_and_url'] = url.count('&')
        features['qty_exclamation_url'] = url.count('!')
        features['qty_space_url'] = url.count(' ')
        features['qty_tilde_url'] = url.count('~')
        features['qty_comma_url'] = url.count(',')
        features['qty_plus_url'] = url.count('+')
        features['qty_asterisk_url'] = url.count('*')
        features['qty_hashtag_url'] = url.count('#')
        features['qty_dollar_url'] = url.count('$')
        features['qty_percent_url'] = url.count('%')
        
        # URL length features (2 features)
        features['qty_tld_url'] = len(extracted.suffix)
        features['length_url'] = len(url)
        
        # Domain features (20 features)
        features['qty_dot_domain'] = domain.count('.')
        features['qty_hyphen_domain'] = domain.count('-')
        features['qty_underline_domain'] = domain.count('_')
        features['qty_slash_domain'] = domain.count('/')
        features['qty_questionmark_domain'] = domain.count('?')
        features['qty_equal_domain'] = domain.count('=')
        features['qty_at_domain'] = domain.count('@')
        features['qty_and_domain'] = domain.count('&')
        features['qty_exclamation_domain'] = domain.count('!')
        features['qty_space_domain'] = domain.count(' ')
        features['qty_tilde_domain'] = domain.count('~')
        features['qty_comma_domain'] = domain.count(',')
        features['qty_plus_domain'] = domain.count('+')
        features['qty_asterisk_domain'] = domain.count('*')
        features['qty_hashtag_domain'] = domain.count('#')
        features['qty_dollar_domain'] = domain.count('$')
        features['qty_percent_domain'] = domain.count('%')
        features['qty_vowels_domain'] = sum(1 for c in domain.lower() if c in 'aeiou')
        features['domain_length'] = len(domain)
        features['domain_in_ip'] = 1 if self._is_ip(domain) else 0
        features['server_client_domain'] = 1 if ('server' in domain.lower() or 'client' in domain.lower()) else 0
        
        # Directory features (17 features)
        features['qty_dot_directory'] = directory.count('.')
        features['qty_hyphen_directory'] = directory.count('-')
        features['qty_underline_directory'] = directory.count('_')
        features['qty_slash_directory'] = directory.count('/')
        features['qty_questionmark_directory'] = directory.count('?')
        features['qty_equal_directory'] = directory.count('=')
        features['qty_at_directory'] = directory.count('@')
        features['qty_and_directory'] = directory.count('&')
        features['qty_exclamation_directory'] = directory.count('!')
        features['qty_space_directory'] = directory.count(' ')
        features['qty_tilde_directory'] = directory.count('~')
        features['qty_comma_directory'] = directory.count(',')
        features['qty_plus_directory'] = directory.count('+')
        features['qty_asterisk_directory'] = directory.count('*')
        features['qty_hashtag_directory'] = directory.count('#')
        features['qty_dollar_directory'] = directory.count('$')
        features['qty_percent_directory'] = directory.count('%')
        features['directory_length'] = len(directory)
        
        # File features (17 features)
        features['qty_dot_file'] = file_part.count('.')
        features['qty_hyphen_file'] = file_part.count('-')
        features['qty_underline_file'] = file_part.count('_')
        features['qty_slash_file'] = file_part.count('/')
        features['qty_questionmark_file'] = file_part.count('?')
        features['qty_equal_file'] = file_part.count('=')
        features['qty_at_file'] = file_part.count('@')
        features['qty_and_file'] = file_part.count('&')
        features['qty_exclamation_file'] = file_part.count('!')
        features['qty_space_file'] = file_part.count(' ')
        features['qty_tilde_file'] = file_part.count('~')
        features['qty_comma_file'] = file_part.count(',')
        features['qty_plus_file'] = file_part.count('+')
        features['qty_asterisk_file'] = file_part.count('*')
        features['qty_hashtag_file'] = file_part.count('#')
        features['qty_dollar_file'] = file_part.count('$')
        features['qty_percent_file'] = file_part.count('%')
        features['file_length'] = len(file_part)
        
        # Parameters features (19 features)
        features['qty_dot_params'] = params.count('.')
        features['qty_hyphen_params'] = params.count('-')
        features['qty_underline_params'] = params.count('_')
        features['qty_slash_params'] = params.count('/')
        features['qty_questionmark_params'] = params.count('?')
        features['qty_equal_params'] = params.count('=')
        features['qty_at_params'] = params.count('@')
        features['qty_and_params'] = params.count('&')
        features['qty_exclamation_params'] = params.count('!')
        features['qty_space_params'] = params.count(' ')
        features['qty_tilde_params'] = params.count('~')
        features['qty_comma_params'] = params.count(',')
        features['qty_plus_params'] = params.count('+')
        features['qty_asterisk_params'] = params.count('*')
        features['qty_hashtag_params'] = params.count('#')
        features['qty_dollar_params'] = params.count('$')
        features['qty_percent_params'] = params.count('%')
        features['params_length'] = len(params)
        features['tld_present_params'] = 1 if any(tld in params for tld in ['.com', '.org', '.net', '.edu']) else 0
        features['qty_params'] = len(parse_qs(params))
        
        # Additional features (19 features) - Set to 0 as we can't extract these without external APIs
        features['email_in_url'] = 1 if '@' in url and '.' in url.split('@')[-1] else 0
        features['time_response'] = 0  # Would need actual DNS lookup
        features['domain_spf'] = 0  # Would need DNS query
        features['asn_ip'] = 0  # Would need IP lookup
        features['time_domain_activation'] = 0  # Would need WHOIS
        features['time_domain_expiration'] = 0  # Would need WHOIS
        features['qty_ip_resolved'] = 0  # Would need DNS lookup
        features['qty_nameservers'] = 0  # Would need DNS query
        features['qty_mx_servers'] = 0  # Would need DNS query
        features['ttl_hostname'] = 0  # Would need DNS query
        features['tls_ssl_certificate'] = 1 if parsed.scheme == 'https' else 0
        features['qty_redirects'] = 0  # Would need HTTP request
        features['url_google_index'] = 0  # Would need Google API
        features['domain_google_index'] = 0  # Would need Google API
        features['url_shortened'] = 1 if any(short in domain for short in ['bit.ly', 'goo.gl', 'tinyurl', 't.co', 'ow.ly']) else 0
        
        return features
    
    def _is_ip(self, text):
        """Check if text is an IP address"""
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        return bool(ip_pattern.match(text))

# Global instance
full_feature_extractor = FullFeatureExtractor()
