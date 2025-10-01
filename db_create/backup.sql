-- --------------------------------------------------------
-- Servidor:                     sysbancadbnew.mysql.dbaas.com.br
-- Versão do servidor:           5.7.32-35-log - Percona Server (GPL), Release 35, Revision 5688520
-- OS do Servidor:               Linux
-- HeidiSQL Versão:              12.11.0.7065
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Copiando estrutura do banco de dados para sysbancadbnew
CREATE DATABASE IF NOT EXISTS `sysbancadbnew` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_general_ci */;
USE `sysbancadbnew`;

-- Copiando estrutura para tabela sysbancadbnew.cadastro_descarrego
CREATE TABLE IF NOT EXISTS `cadastro_descarrego` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `areas` text COLLATE latin1_general_ci,
  `modalidade` text COLLATE latin1_general_ci,
  `extracao` text COLLATE latin1_general_ci,
  `limite` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.cotacao_definida
CREATE TABLE IF NOT EXISTS `cotacao_definida` (
  `nome` int(11) DEFAULT NULL,
  `milhar` int(11) DEFAULT NULL,
  `centena` int(11) DEFAULT NULL,
  `dezena` int(11) DEFAULT NULL,
  `grupo` int(11) DEFAULT NULL,
  `terno_de_grupo` int(11) DEFAULT NULL,
  `terno_de_dezena` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.descarregos
CREATE TABLE IF NOT EXISTS `descarregos` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `bilhete` int(11) NOT NULL,
  `extracao` text COLLATE latin1_general_ci NOT NULL,
  `valor_apostado` float NOT NULL,
  `valor_excedente` float NOT NULL,
  `numeros` text COLLATE latin1_general_ci NOT NULL,
  `data` timestamp NOT NULL,
  `modalidade` text COLLATE latin1_general_ci NOT NULL,
  `premio_total` float DEFAULT NULL,
  `premio_excedente` float DEFAULT NULL,
  `tipo_premio` varchar(50) COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.extracao_area
CREATE TABLE IF NOT EXISTS `extracao_area` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `area` varchar(100) COLLATE latin1_general_ci DEFAULT NULL,
  `extracao` varchar(100) COLLATE latin1_general_ci DEFAULT NULL,
  `ativar` varchar(10) COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tblpessoa
CREATE TABLE IF NOT EXISTS `tblpessoa` (
  `nome` varchar(20) COLLATE latin1_general_ci NOT NULL,
  `sobrenome` varchar(20) COLLATE latin1_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_apostas
CREATE TABLE IF NOT EXISTS `tb_apostas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vendedor` varchar(50) COLLATE latin1_general_ci NOT NULL,
  `data_atual` date NOT NULL,
  `hora_atual` time NOT NULL,
  `valor_total` decimal(10,2) NOT NULL,
  `horario_selecionado` varchar(50) COLLATE latin1_general_ci DEFAULT NULL,
  `apostas` text COLLATE latin1_general_ci NOT NULL,
  `pre_datar` tinyint(1) NOT NULL DEFAULT '0',
  `data_agendada` date DEFAULT NULL,
  `area` varchar(25) COLLATE latin1_general_ci DEFAULT NULL,
  `nsu` varchar(50) COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=273 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_apostas_excluidas
CREATE TABLE IF NOT EXISTS `tb_apostas_excluidas` (
  `id` int(11) NOT NULL,
  `area` varchar(50) COLLATE latin1_general_ci DEFAULT NULL,
  `vendedor` varchar(50) COLLATE latin1_general_ci DEFAULT NULL,
  `data_atual` date DEFAULT NULL,
  `hora_atual` time DEFAULT NULL,
  `valor_total` float DEFAULT NULL,
  `extracao` varchar(50) COLLATE latin1_general_ci DEFAULT NULL,
  `apostas` text COLLATE latin1_general_ci,
  `pre_datar` tinyint(1) DEFAULT NULL,
  `data_agendada` date DEFAULT NULL,
  `data_exclusao` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_apostas_premiadas
CREATE TABLE IF NOT EXISTS `tb_apostas_premiadas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `vendedor` text COLLATE latin1_general_ci NOT NULL,
  `data_atual` date NOT NULL,
  `hora_atual` time NOT NULL,
  `valor_total` float NOT NULL,
  `horario_selecionado` varchar(50) COLLATE latin1_general_ci NOT NULL,
  `apostas` text COLLATE latin1_general_ci NOT NULL,
  `pre_datar` tinyint(1) NOT NULL DEFAULT '0',
  `data_agendada` date DEFAULT NULL,
  `area` varchar(25) COLLATE latin1_general_ci NOT NULL,
  `valor_premio` text COLLATE latin1_general_ci,
  `impresso` tinyint(1) DEFAULT '0',
  `numero_bilhete` int(11) NOT NULL,
  `pago` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_bilhete` (`numero_bilhete`),
  UNIQUE KEY `unique_numero_bilhete` (`numero_bilhete`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_area
CREATE TABLE IF NOT EXISTS `tb_area` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `RegiaoArea` varchar(20) COLLATE latin1_general_ci NOT NULL,
  `DescArea` varchar(20) COLLATE latin1_general_ci NOT NULL,
  `AtivarArea` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_AreaCotacao
CREATE TABLE IF NOT EXISTS `tb_AreaCotacao` (
  `idCotArea` int(11) NOT NULL AUTO_INCREMENT,
  `area` varchar(50) COLLATE latin1_general_ci NOT NULL,
  `extracao` varchar(50) COLLATE latin1_general_ci NOT NULL,
  `modalidade` varchar(50) COLLATE latin1_general_ci NOT NULL,
  `cotacao` int(11) NOT NULL,
  `AtivarAreaCotacao` int(4) NOT NULL,
  PRIMARY KEY (`idCotArea`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_AreaLimite
CREATE TABLE IF NOT EXISTS `tb_AreaLimite` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `area_limite` varchar(15) COLLATE latin1_general_ci NOT NULL,
  `extracao_area_limite` varchar(15) COLLATE latin1_general_ci NOT NULL,
  `modalidade_area_limite` varchar(15) COLLATE latin1_general_ci NOT NULL,
  `limite_area_palpite` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_coletas
CREATE TABLE IF NOT EXISTS `tb_coletas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `coletor` varchar(50) COLLATE latin1_general_ci DEFAULT NULL,
  `data` date DEFAULT NULL,
  `valor_coleta` float DEFAULT NULL,
  `valor_debito` float DEFAULT NULL,
  `vendedor` text COLLATE latin1_general_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_ColetaVendedor
CREATE TABLE IF NOT EXISTS `tb_ColetaVendedor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data_inicial` date NOT NULL,
  `data_final` date NOT NULL,
  `area_coleta` varchar(15) COLLATE latin1_general_ci NOT NULL,
  `coletor` varchar(15) COLLATE latin1_general_ci NOT NULL,
  `coleta_vendedor` varchar(15) COLLATE latin1_general_ci NOT NULL,
  `tipo_coleta` text COLLATE latin1_general_ci NOT NULL,
  `status` text COLLATE latin1_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_coletor
CREATE TABLE IF NOT EXISTS `tb_coletor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome_coletor` varchar(15) COLLATE latin1_general_ci NOT NULL,
  `area` varchar(15) COLLATE latin1_general_ci NOT NULL,
  `login` varchar(10) COLLATE latin1_general_ci NOT NULL,
  `senha` varchar(10) COLLATE latin1_general_ci NOT NULL,
  `ativar_coletor` text COLLATE latin1_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_comissaoArea
CREATE TABLE IF NOT EXISTS `tb_comissaoArea` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `area` varchar(100) COLLATE latin1_general_ci NOT NULL,
  `modalidade` text COLLATE latin1_general_ci NOT NULL,
  `comissao` float NOT NULL,
  `ativar` varchar(10) COLLATE latin1_general_ci NOT NULL,
  `vendedor` text COLLATE latin1_general_ci,
  `extracao` text COLLATE latin1_general_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_extracao
CREATE TABLE IF NOT EXISTS `tb_extracao` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `extracao` varchar(30) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `fechamento` time(4) NOT NULL,
  `premiacao` int(2) NOT NULL,
  `DiasExtracao` varchar(100) COLLATE latin1_general_ci NOT NULL,
  `ativo` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_modalidade
CREATE TABLE IF NOT EXISTS `tb_modalidade` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `modalidade` varchar(50) COLLATE latin1_general_ci NOT NULL,
  `unidade` int(11) NOT NULL,
  `LimitePorAposta` int(11) NOT NULL,
  `cotacao` float NOT NULL,
  `ativar_area` tinyint(1) NOT NULL,
  `LimiteDescarrego` float DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `modalidade` (`modalidade`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_numeros_cotados
CREATE TABLE IF NOT EXISTS `tb_numeros_cotados` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `numero` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_regiao
CREATE TABLE IF NOT EXISTS `tb_regiao` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `desc_regiao` varchar(20) COLLATE latin1_general_ci NOT NULL,
  `ativo` tinyint(1) NOT NULL,
  `regiao` varchar(20) COLLATE latin1_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_Relatorios
CREATE TABLE IF NOT EXISTS `tb_Relatorios` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` varchar(50) COLLATE latin1_general_ci NOT NULL,
  `tabela` varchar(50) COLLATE latin1_general_ci NOT NULL,
  `acao` varchar(30) COLLATE latin1_general_ci NOT NULL,
  `id_linha` int(11) NOT NULL,
  `linha` text COLLATE latin1_general_ci NOT NULL,
  `data` date NOT NULL,
  `horario` time NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=255 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_resultados
CREATE TABLE IF NOT EXISTS `tb_resultados` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `extracao` varchar(255) COLLATE latin1_general_ci DEFAULT NULL,
  `data` date NOT NULL,
  `premio_1` text COLLATE latin1_general_ci NOT NULL,
  `premio_2` text COLLATE latin1_general_ci NOT NULL,
  `premio_3` text COLLATE latin1_general_ci NOT NULL,
  `premio_4` text COLLATE latin1_general_ci NOT NULL,
  `premio_5` text COLLATE latin1_general_ci NOT NULL,
  `premio_6` text COLLATE latin1_general_ci NOT NULL,
  `premio_7` text COLLATE latin1_general_ci NOT NULL,
  `premio_8` text COLLATE latin1_general_ci,
  `premio_9` text COLLATE latin1_general_ci,
  `premio_10` text COLLATE latin1_general_ci,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_users
CREATE TABLE IF NOT EXISTS `tb_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE latin1_general_ci NOT NULL,
  `senha` varchar(255) COLLATE latin1_general_ci NOT NULL,
  `acesso_usuario` tinyint(1) DEFAULT '0',
  `acesso_modalidade` tinyint(1) DEFAULT '0',
  `acesso_regiao` tinyint(1) DEFAULT '0',
  `acesso_extracao` tinyint(1) DEFAULT '0',
  `acesso_area_extracao` tinyint(1) DEFAULT '0',
  `acesso_area_cotacao` tinyint(1) DEFAULT '0',
  `acesso_area_comissao_modalidade` tinyint(1) DEFAULT '0',
  `acesso_coletor` tinyint(1) DEFAULT '0',
  `acesso_vendedor` tinyint(1) DEFAULT '0',
  `acesso_vendas_por_periodo_operador` tinyint(1) DEFAULT '0',
  `acesso_relatorio_geral_de_vendas` tinyint(1) DEFAULT '0',
  `acesso_numeros_cotados` tinyint(1) DEFAULT '0',
  `acesso_programacao_extracao` tinyint(1) DEFAULT '0',
  `acesso_descarrego` tinyint(1) DEFAULT '0',
  `acesso_cancelamento_fora_do_horario` tinyint(1) DEFAULT '0',
  `acesso_administracao` tinyint(1) DEFAULT '0',
  `acesso_area` tinyint(1) NOT NULL DEFAULT '0',
  `ativo` text COLLATE latin1_general_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.tb_vendedores
CREATE TABLE IF NOT EXISTS `tb_vendedores` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) COLLATE latin1_general_ci NOT NULL,
  `username` varchar(50) COLLATE latin1_general_ci NOT NULL,
  `senha` varchar(255) COLLATE latin1_general_ci NOT NULL,
  `serial` varchar(100) COLLATE latin1_general_ci DEFAULT NULL,
  `area` varchar(25) COLLATE latin1_general_ci DEFAULT NULL,
  `regiao` varchar(50) COLLATE latin1_general_ci DEFAULT NULL,
  `ativo` enum('sim','nao') COLLATE latin1_general_ci DEFAULT NULL,
  `comissao` decimal(5,2) DEFAULT NULL,
  `cancelar_poule` enum('sim','nao') COLLATE latin1_general_ci DEFAULT NULL,
  `exibe_comissao` enum('sim','nao') COLLATE latin1_general_ci DEFAULT NULL,
  `limite_venda` decimal(10,2) DEFAULT NULL,
  `tipo_limite` varchar(50) COLLATE latin1_general_ci DEFAULT NULL,
  `grade` varchar(50) COLLATE latin1_general_ci DEFAULT NULL,
  `teste` varchar(100) COLLATE latin1_general_ci DEFAULT NULL,
  `comissao_retida` decimal(5,2) DEFAULT NULL,
  `exibe_premiacao` tinyint(1) DEFAULT '0',
  `cotacao_definida` varchar(255) COLLATE latin1_general_ci DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `serial` (`serial`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para tabela sysbancadbnew.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `cpf` varchar(11) COLLATE latin1_general_ci NOT NULL,
  `email` varchar(255) COLLATE latin1_general_ci NOT NULL,
  `celular` varchar(15) COLLATE latin1_general_ci DEFAULT NULL,
  `senha` varchar(255) COLLATE latin1_general_ci NOT NULL,
  PRIMARY KEY (`cpf`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;

-- Exportação de dados foi desmarcado.

-- Copiando estrutura para trigger sysbancadbnew.trg_prevent_empty_modalidade
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='';
DELIMITER //
CREATE TRIGGER trg_prevent_empty_modalidade
BEFORE INSERT ON tb_modalidade
FOR EACH ROW
BEGIN
  IF TRIM(NEW.modalidade) = '' THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'O campo modalidade não pode ser vazio';
  END IF;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Copiando estrutura para trigger sysbancadbnew.trg_prevent_empty_modalidade_update
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='';
DELIMITER //
CREATE TRIGGER trg_prevent_empty_modalidade_update
BEFORE UPDATE ON tb_modalidade
FOR EACH ROW
BEGIN
  IF TRIM(NEW.modalidade) = '' THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'O campo modalidade não pode ser vazio';
  END IF;
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
