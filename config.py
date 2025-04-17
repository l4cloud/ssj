import json

KNOWN_PARAMS = (
    "AddKeysToAgent",
    "AddressFamily",
    "BatchMode",
    "BindAddress",
    "CanonicalDomains",
    "CanonicalizeFallbackLocal",
    "CanonicalizeHostname",
    "CanonicalizeMaxDots",
    "CanonicalizePermittedCNAMEs",
    "CertificateFile",
    "ChallengeResponseAuthentication",
    "CheckHostIP",
    "Cipher",
    "Ciphers",
    "ClearAllForwardings",
    "Compression",
    "CompressionLevel",
    "ConnectionAttempts",
    "ConnectTimeout",
    "ControlMaster",
    "ControlPath",
    "ControlPersist",
    "DynamicForward",
    "EscapeChar",
    "ExitOnForwardFailure",
    "FingerprintHash",
    "ForwardAgent",
    "ForwardX11",
    "ForwardX11Timeout",
    "ForwardX11Trusted",
    "GatewayPorts",
    "GlobalKnownHostsFile",
    "GSSAPIAuthentication",
    "GSSAPIKeyExchange",
    "GSSAPIClientIdentity",
    "GSSAPIDelegateCredentials",
    "GSSAPIRenewalForcesRekey",
    "GSSAPITrustDns",
    "GSSAPIKexAlgorithms",
    "HashKnownHosts",
    "Host",
    "HostbasedAuthentication",
    "HostbasedKeyTypes",
    "HostKeyAlgorithms",
    "HostKeyAlias",
    "HostName",
    "IdentitiesOnly",
    "IdentityAgent",
    "IdentityFile",
    "Include",
    "IPQoS",
    "KbdInteractiveAuthentication",
    "KbdInteractiveDevices",
    "KexAlgorithms",
    "LocalCommand",
    "LocalForward",
    "LogLevel",
    "MACs",
    "Match",
    "NoHostAuthenticationForLocalhost",
    "NumberOfPasswordPrompts",
    "PasswordAuthentication",
    "PermitLocalCommand",
    "PKCS11Provider",
    "Port",
    "PreferredAuthentications",
    "Protocol",
    "ProxyCommand",
    "ProxyJump",
    "ProxyUseFdpass",
    "PubkeyAcceptedKeyTypes",
    "PubkeyAuthentication",
    "RekeyLimit",
    "RemoteForward",
    "RequestTTY",
    "RhostsRSAAuthentication",
    "RSAAuthentication",
    "SendEnv",
    "ServerAliveInterval",
    "ServerAliveCountMax",
    "StreamLocalBindMask",
    "StreamLocalBindUnlink",
    "StrictHostKeyChecking",
    "TCPKeepAlive",
    "Tunnel",
    "TunnelDevice",
    "UpdateHostKeys",
    "UsePrivilegedPort",
    "User",
    "UserKnownHostsFile",
    "VerifyHostKeyDNS",
    "VisualHostKey",
    "XAuthLocation"
)

known_params = [x.lower() for x in KNOWN_PARAMS]


class ConfigLine:
    def __init__(self, host: str, key: str, value: str):
        self.host = host
        self.key = value
        if key.lower() in known_params:
            self.key = key
            self.content = {
                "host": host,
                key: value
            }
        else:
            raise Exception("Invalid config line value: " + key)


class Host:
    def __init__(self, name: str):
        self.name = name
        self.config = []

    def add_config(self, line):
        self.config.append(line)
