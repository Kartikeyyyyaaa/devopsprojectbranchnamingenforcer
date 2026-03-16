# Puppet manifest – Branch Naming Convention Enforcer
# Installs Python, copies the enforcer, and sets up git hooks on dev machines

class branch_enforcer {

  # Ensure Python 3 is available
  package { 'python3':
    ensure => installed,
  }

  package { 'python3-pip':
    ensure  => installed,
    require => Package['python3'],
  }

  # Install pytest for local testing
  exec { 'install-pytest':
    command => '/usr/bin/pip3 install pytest pytest-cov flake8',
    unless  => '/usr/bin/pip3 show pytest',
    require => Package['python3-pip'],
  }

  # Ensure project directory exists
  file { '/opt/branch-enforcer':
    ensure => directory,
    owner  => 'root',
    group  => 'root',
    mode   => '0755',
  }

  # Copy main enforcer script
  file { '/opt/branch-enforcer/branch_enforcer.py':
    ensure  => file,
    source  => 'puppet:///modules/branch_enforcer/branch_enforcer.py',
    owner   => 'root',
    group   => 'root',
    mode    => '0755',
    require => File['/opt/branch-enforcer'],
  }

  # Symlink for global use
  file { '/usr/local/bin/branch-enforcer':
    ensure  => link,
    target  => '/opt/branch-enforcer/branch_enforcer.py',
    require => File['/opt/branch-enforcer/branch_enforcer.py'],
  }
}

include branch_enforcer
