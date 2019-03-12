/*
Terraform Config  - SFTP Server via DigitalOcean Droplet
Written by Matt Bromiley (@mbromileyDFIR - 505 Forensics)

You'll need to configure the following within the tfvars file:
 - DigitalOcean API Key (var: do_token)
 - List of SSH Keys, preferably already in DO profile (var: ssh_keys)
*/

# Variable import
variable do_token {}
variable ssh_keys {
  type = "list"
}

# DigitalOcean initialization
provider digitalocean {
    token = "${var.do_token}"
}

# Password generator
# This password will stay as part of the terraform state until destroyed.
resource "random_string" "password" {
  length = 20
  special = true
}

# The following droplet is a $20/mo droplet. Feel free to change the slug if you need a smaller or larger size.
resource "digitalocean_droplet" "sftp-server" {
    image      = "ubuntu-18-04-x64"
    name       = "sftp-server"
    region     = "nyc1"
    size       = "s-2vcpu-4gb"
    ssh_keys   = "${var.ssh_keys}"

    connection {
      type          = "ssh"
      user          = "root"
      private_key   = <path_to_private_key>
    }
    # The steps outlined below were taken directly from https://www.digitalocean.com/community/tutorials/how-to-enable-sftp-without-shell-access-on-ubuntu-18-04
    # I didn't have a problem with their setup, but again, I wanted this to be quick.
    provisioner "remote-exec" {
      inline = [
        "mkdir -p /var/sftp/uploads",
        "chown root:root /var/sftp",
        "chmod 755 /var/sftp",
        "useradd -d /home/sftp sftp",
        "echo sftp:\"${random_string.password.result}\" | chpasswd", #Must maintain quotes or else command will fail
        "chown sftp:sftp /var/sftp/uploads",
        "echo Match User sftp >> /etc/ssh/sshd_config",
        "echo ForceCommand internal-sftp >> /etc/ssh/sshd_config",
        "echo PasswordAuthentication yes >> /etc/ssh/sshd_config",
        "echo ChrootDirectory /var/sftp >> /etc/ssh/sshd_config",
        "echo PermitTunnel no >> /etc/ssh/sshd_config",
        "echo AllowAgentForwarding no >> /etc/ssh/sshd_config",
        "echo AllowTcpForwarding no >> /etc/ssh/sshd_config",
        "echo X11Forwarding no >> /etc/ssh/sshd_config",
        "sed -i 's/ChallengeResponseAuthentication no/ChallengeResponseAuthentication yes/g' /etc/ssh/sshd_config",
        "systemctl restart sshd"
      ]
    }
}

# Output is block text to provide updated login info and stats to the user. If not needed, remove any of these.
output "SFTP Config" {
  value = <<SFTPDETAILS

  IP Address: ${digitalocean_droplet.sftp-server.ipv4_address}
  Username: sftp
  Password: ${random_string.password.result}
  Monthly Price: $ ${digitalocean_droplet.sftp-server.price_monthly}

  KAPE Line: --scs ${digitalocean_droplet.sftp-server.ipv4_address} --scu sftp --scpw "${random_string.password.result}"
  SFTP Command: sftp sftp@${digitalocean_droplet.sftp-server.ipv4_address}
  SFTPDETAILS
}