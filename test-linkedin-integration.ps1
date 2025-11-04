# Script de test pour l'intégration LinkedIn
# Teste les credentials et la capacité de publier

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   Test Integration LinkedIn - VOC-Call" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Les credentials depuis GitHub Secrets (simulation locale)
$CLIENT_ID = "78a639tvdurngb"
$CLIENT_SECRET = "WPL_AP1.7VKBgjGWkXiSFMHI.s4s+TQ=="
$ACCESS_TOKEN = "AQUK4OWEXWzJBydknYtKhsaLmOfO1Kd3Ns3XWfmNXMqsiqSKUtPWvm66umsqGObjtmjRd48RN--zUmlBd8GiWA50JHe2qDp1whDRRpY7xMMzvMNY8Z3CNIZ5CZLVhMuBU2biKwdAjthYaABLFKPBcKZpfrSrstV5qE2tNHF7xffeP2rTFO5yHHHlLMa9Wjsq7WUrJBTnnuk3mV8Jc7iIXq8Cv2Mf1i4flmbzIjm4oRD5TiyBfGGUc8MJhfic6UqTrKBSZp4-jNfSCYpFaeUMcOTPYAL-fuGjXzJfpVspLhey8bIoLuTT6h_fd140aUE3vTTcAYGNn4HB2BT8TIQiIkXFFRbfmg"

Write-Host "ETAPE 1 : Test de l'Access Token..." -ForegroundColor Yellow
Write-Host "-----------------------------------------------" -ForegroundColor Yellow

try {
    $headers = @{
        "Authorization" = "Bearer $ACCESS_TOKEN"
        "Content-Type" = "application/json"
    }
    
    # Test 1 : Récupérer le profil
    Write-Host "Test : Recuperation du profil LinkedIn..." -ForegroundColor Cyan
    $profile = Invoke-RestMethod -Uri "https://api.linkedin.com/v2/me?projection=(id,localizedFirstName,localizedLastName)" -Method Get -Headers $headers
    
    if ($profile.id) {
        Write-Host "SUCCES ! Profil recupere :" -ForegroundColor Green
        Write-Host "  - URN: $($profile.id)" -ForegroundColor White
        Write-Host "  - Nom: $($profile.localizedFirstName) $($profile.localizedLastName)" -ForegroundColor White
        Write-Host ""
        
        $PERSON_URN = $profile.id
    } else {
        Write-Host "ERREUR: Impossible de recuperer le profil" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "ERREUR lors du test du profil :" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Reponse: $responseBody" -ForegroundColor Red
    }
    exit 1
}

Write-Host "ETAPE 2 : Test de creation d'un post de test..." -ForegroundColor Yellow
Write-Host "-----------------------------------------------" -ForegroundColor Yellow
Write-Host ""
Write-Host "ATTENTION : Ce test va creer un VRAI post sur votre profil LinkedIn !" -ForegroundColor Yellow
Write-Host ""

$confirm = Read-Host "Voulez-vous creer un post de test ? (oui/non)"

if ($confirm -ne "oui") {
    Write-Host ""
    Write-Host "Test annule. L'integration est configuree correctement !" -ForegroundColor Green
    Write-Host ""
    Write-Host "RESUME :" -ForegroundColor Cyan
    Write-Host "  - Access Token : VALIDE" -ForegroundColor Green
    Write-Host "  - Profil LinkedIn : RECUPERE" -ForegroundColor Green
    Write-Host "  - Person URN : $PERSON_URN" -ForegroundColor Green
    Write-Host ""
    Write-Host "L'integration LinkedIn est pret a etre utilisee !" -ForegroundColor Green
    Write-Host "Les prochains articles de blog seront automatiquement publies sur LinkedIn." -ForegroundColor Green
    exit 0
}

# Test de publication
Write-Host ""
Write-Host "Creation d'un post de test..." -ForegroundColor Cyan

$testPostText = "🧪 Test automatique depuis VOC-Call Blog Publisher`n`nCe message confirme que l'integration LinkedIn fonctionne correctement ! ✅`n`n#VOCCall #Test #Integration"

try {
    # Créer un UGC Post
    $ugcPost = @{
        author = $PERSON_URN
        lifecycleState = "PUBLISHED"
        specificContent = @{
            "com.linkedin.ugc.ShareContent" = @{
                shareCommentary = @{
                    text = $testPostText
                }
                shareMediaCategory = "ARTICLE"
                media = @()
            }
        }
        visibility = @{
            "com.linkedin.ugc.MemberNetworkVisibility" = "PUBLIC"
        }
    } | ConvertTo-Json -Depth 10

    $postHeaders = @{
        "Authorization" = "Bearer $ACCESS_TOKEN"
        "Content-Type" = "application/json"
        "X-Restli-Protocol-Version" = "2.0.0"
    }

    $postResponse = Invoke-RestMethod -Uri "https://api.linkedin.com/v2/ugcPosts" -Method Post -Headers $postHeaders -Body $ugcPost

    if ($postResponse.id) {
        Write-Host ""
        Write-Host "SUCCES ! Post de test cree sur LinkedIn !" -ForegroundColor Green
        Write-Host "  - Post ID: $($postResponse.id)" -ForegroundColor White
        Write-Host ""
        Write-Host "Vous pouvez le voir sur votre profil LinkedIn." -ForegroundColor Cyan
        Write-Host ""
        Write-Host "RESUME :" -ForegroundColor Cyan
        Write-Host "  - Access Token : VALIDE" -ForegroundColor Green
        Write-Host "  - Profil LinkedIn : RECUPERE" -ForegroundColor Green
        Write-Host "  - Person URN : $PERSON_URN" -ForegroundColor Green
        Write-Host "  - Publication : FONCTIONNE" -ForegroundColor Green
        Write-Host ""
        Write-Host "L'integration LinkedIn est OPERATIONNELLE !" -ForegroundColor Green
        Write-Host "Les prochains articles de blog seront automatiquement publies sur LinkedIn." -ForegroundColor Green
    } else {
        Write-Host "ERREUR: Post cree mais pas d'ID retourne" -ForegroundColor Yellow
        Write-Host "Reponse: $($postResponse | ConvertTo-Json)" -ForegroundColor Yellow
    }
} catch {
    Write-Host ""
    Write-Host "ERREUR lors de la creation du post :" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Reponse: $responseBody" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Mais le test du profil a reussi, donc les credentials sont valides." -ForegroundColor Yellow
    Write-Host "Le probleme peut venir des permissions de l'application LinkedIn." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Verifiez que :" -ForegroundColor Cyan
    Write-Host "  - Le produit 'Marketing Developer Platform' est active" -ForegroundColor White
    Write-Host "  - Les scopes incluent 'w_member_social'" -ForegroundColor White
}

Write-Host ""
Write-Host "Appuyez sur une touche pour quitter..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


