# Script rapide pour obtenir l'Access Token avec le code fourni

$CLIENT_ID = "78a639tvdurngb"
$CLIENT_SECRET = "WPL_AP1.7VKBgjGWkXiSFMHI.s4s+TQ=="
$REDIRECT_URI = "http://localhost:3000"
$AUTH_CODE = "AQQg3W-T_1_s9YiIErtQKD39cz28n_Nx-8zaFsGY6v_cZa1LmyBQC_WbOnRQopYCR59D3faXpLlZiKecAv8LSBaoR04tKeYzWdIZvd4TcN3-AmAs-fWosnDXQ8joR8tg2dAGs19CSwqJlnqtZjlJ-hbRVeHLwY93OVsQunUtUALLtI-M2d4a3xHewyjsy3r3eHlDlkUUpoWmCrbNfHU"

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   Obtention de l'Access Token LinkedIn" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Echange du code contre un Access Token..." -ForegroundColor Yellow
Write-Host ""

try {
    $body = @{
        grant_type = "authorization_code"
        code = $AUTH_CODE
        redirect_uri = $REDIRECT_URI
        client_id = $CLIENT_ID
        client_secret = $CLIENT_SECRET
    }

    $response = Invoke-RestMethod -Uri "https://www.linkedin.com/oauth/v2/accessToken" -Method Post -Body $body -ContentType "application/x-www-form-urlencoded"

    if ($response.access_token) {
        Write-Host ""
        Write-Host "SUCCES ! Access Token obtenu :" -ForegroundColor Green
        Write-Host "================================================" -ForegroundColor Green
        Write-Host $response.access_token -ForegroundColor White
        Write-Host "================================================" -ForegroundColor Green
        Write-Host ""
        $days = [math]::Floor($response.expires_in / 86400)
        Write-Host "Expire dans : $days jours" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "IMPORTANT : Ajoutez cette valeur dans GitHub Secrets :" -ForegroundColor Yellow
        Write-Host "   Nom du secret : LINKEDIN_ACCESS_TOKEN" -ForegroundColor White
        Write-Host "   Valeur : (copiez le token ci-dessus)" -ForegroundColor White
        Write-Host ""

        # Recuperer le Person URN
        Write-Host "Recuperation du Person URN..." -ForegroundColor Cyan
        try {
            $headers = @{
                "Authorization" = "Bearer $($response.access_token)"
                "Content-Type" = "application/json"
            }
            $profile = Invoke-RestMethod -Uri "https://api.linkedin.com/v2/me?projection=(id,localizedFirstName,localizedLastName)" -Method Get -Headers $headers
            
            if ($profile.id) {
                Write-Host ""
                Write-Host "Person URN: $($profile.id)" -ForegroundColor Green
                if ($profile.localizedFirstName) {
                    Write-Host "   Profil: $($profile.localizedFirstName) $($profile.localizedLastName)" -ForegroundColor Cyan
                }
                Write-Host ""
                Write-Host "Optionnel : Ajoutez cette valeur dans GitHub Secrets :" -ForegroundColor Yellow
                Write-Host "   Nom du secret : LINKEDIN_PERSON_URN" -ForegroundColor White
                Write-Host "   Valeur : $($profile.id)" -ForegroundColor White
                Write-Host ""
            }
        } catch {
            Write-Host "Impossible de recuperer le Person URN (non critique)" -ForegroundColor Yellow
        }

        # Sauvegarder dans un fichier pour faciliter la copie
        $output = @"
================================================
   CREDENTIALS LINKEDIN - VOC-Call
================================================

LINKEDIN_ACCESS_TOKEN=$($response.access_token)

LINKEDIN_PERSON_URN=$($profile.id)

Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Expire dans: $days jours

================================================
"@

        $output | Out-File -FilePath "linkedin-credentials.txt" -Encoding UTF8
        Write-Host "Credentials sauvegardes dans: linkedin-credentials.txt" -ForegroundColor Green
        Write-Host ""

    } else {
        Write-Host "ERREUR: Pas de token dans la reponse" -ForegroundColor Red
        Write-Host "Reponse : $($response | ConvertTo-Json)" -ForegroundColor Red
    }
} catch {
    Write-Host "ERREUR lors de la recuperation du token :" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Reponse d'erreur : $responseBody" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Depannage :" -ForegroundColor Yellow
    Write-Host "- Verifiez que le code n'a pas expire (utilisez-le rapidement)" -ForegroundColor White
    Write-Host "- Verifiez que Client ID et Secret sont corrects" -ForegroundColor White
    Write-Host "- Verifiez que la Redirect URI correspond exactement" -ForegroundColor White
}

Write-Host ""
Write-Host "Appuyez sur une touche pour quitter..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


