### 2021-05-03

## VM: Configurazione di rete

- **NAT**\
    -> **DHCP**: virtualizzatore\
    -> tutte le macchine hanno lo stesso indirizzo IP di classe A (10.x.x.x)
- **NAT Network**\
    -> **DHCP**: virtualizzatore
    -> le macchine hanno indirizzi IP diversi, poichè le VM fanno parte della stessa rete (sono )
- **Bridge**\
    -> **DHCP**: si delega, in base al contesto _(indirizzi IP statici/assegnati dal DHCP del router)_\
    -> non si fa differenza tra VM e macchine fisiche

---

### 2021-04-23

## STACK DevSecOps

- apps -> ini
- rete -> NetworkAdmin - sri
- OS + HW -> SystemAdmin - sri/tpi/ini

## POWERSHELL
- linguaggio ufficiale microsoft
- permette di utilizzare più linguaggi
- case insensitive
- Stack
    - powershell
    - .NET Framework 
        > - equivalente di JVM per Java
        > - fa parte dell'OS
    - OS
- **cmdlet** -> programmi già fatti, raggruppati in moduli (librerie)
- processi (a volte fanno partire dei thread)
- svchost -> hub per molti processi

---

### PARAMETRI
```powershell
param (
    [string]$foldername = "../flussi/"
    , [Parameter(Mandatory=$false)]  [ValidateSet("QUASYS", "PROSYS")][String]$ambiente = "QUASYS"
    , [Parameter(Mandatory=$false)]  [ValidateSet($false, $true)][String]$boolexesql = $false
)
```

### FUNZIONI
```powershell
function fnGetConfiguration {
    $ambiente_t = [String]$args[0] # [String]$args -> parametri della funzione
    <# funzione #>
}
```

### COMMENTI
```powershell
<#
multiline
comment
#>

# single line comment
```

### STRINGHE

```powershell
$var = "<3"
Write-Host "hello, world! $var" # Write-Host -> print
Write-Host "Lorem ipsum $var something" -ForegroundColor Cyan # -ForegroundColor Cyan  -> colored text omg cool!!!
Write-Host "Lorem ipsum" + $var + "something" -ForegroundColor Purple # another concat method in case you didn't want to use the first one
```