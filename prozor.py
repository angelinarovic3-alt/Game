import math
import random
import pygame

pygame.init()

W, H = 320, 180
SKALA = 3
prozor = pygame.display.set_mode((W * SKALA, H * SKALA))
pygame.display.set_caption("Zamak — Sobe, Gornji sprat i Priča")
canvas = pygame.Surface((W, H))
sat = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 8)

SOBA_GRANICE = (48, W - 48, 38, H - 28)
LED_ZONA = pygame.Rect(112, 76, 96, 48)


def napravi_sobe():
    return {
        "hol": {
            "naziv": "Glavni hol",
            "prolazi": [
                {
                    "rect": pygame.Rect(152, 152, 16, 10),
                    "cilj_scena": "spolja",
                    "cilj_x": 163.0,
                    "cilj_y": 78.0,
                    "poruka": "Izasao si napolje.",
                    "zahteva_ciscenje": False,
                },
                {
                    "rect": pygame.Rect(44, 82, 8, 16),
                    "cilj_scena": "biblioteka",
                    "cilj_x": 258.0,
                    "cilj_y": 90.0,
                    "poruka": "Ulazis u staru biblioteku.",
                    "zahteva_ciscenje": False,
                },
                {
                    "rect": pygame.Rect(268, 82, 8, 16),
                    "cilj_scena": "odaja",
                    "cilj_x": 62.0,
                    "cilj_y": 90.0,
                    "poruka": "Ulazis u gornju odaju.",
                    "zahteva_ciscenje": True,
                },
            ],
            "prepreke": [
                pygame.Rect(112, 74, 10, 14),
                pygame.Rect(198, 74, 10, 14),
            ],
            "baklje": [(76, 72), (244, 72), (160, 52)],
            "objekti": [
                {
                    "id": "sto_hol",
                    "x": 146,
                    "y": 94,
                    "w": 24,
                    "h": 10,
                    "boja": (96, 64, 42),
                    "naziv": "Stari sto",
                    "tekst_pre": "Na stolu pise: 'Desna vrata se otvaraju tek kad utisas senke.'",
                    "tekst_posle": "Na stolu sada stoji urezan znak: 'Kljuc istine je u odaji.'",
                }
            ],
        },
        "biblioteka": {
            "naziv": "Stara biblioteka",
            "prolazi": [
                {
                    "rect": pygame.Rect(268, 82, 8, 16),
                    "cilj_scena": "hol",
                    "cilj_x": 60.0,
                    "cilj_y": 90.0,
                    "poruka": "Vratio si se u glavni hol.",
                    "zahteva_ciscenje": False,
                },
            ],
            "prepreke": [
                pygame.Rect(95, 55, 42, 8),
                pygame.Rect(95, 118, 42, 8),
            ],
            "baklje": [(85, 68), (185, 68)],
            "objekti": [
                {
                    "id": "ognjiste_bib",
                    "x": 175,
                    "y": 114,
                    "w": 16,
                    "h": 12,
                    "boja": (185, 85, 35),
                    "naziv": "Ognjiste",
                    "tekst_pre": "Vatra ti vraca snagu (+30 HP).",
                    "tekst_posle": "Zar jos tinja i cuva ti ledja.",
                }
            ],
        },
        "odaja": {
            "naziv": "Odaja senki",
            "prolazi": [
                {
                    "rect": pygame.Rect(44, 82, 8, 16),
                    "cilj_scena": "hol",
                    "cilj_x": 252.0,
                    "cilj_y": 90.0,
                    "poruka": "Vratio si se u glavni hol.",
                    "zahteva_ciscenje": False,
                },
                {
                    "rect": pygame.Rect(154, 36, 12, 8),
                    "cilj_scena": "gornji_sprat",
                    "cilj_x": 160.0,
                    "cilj_y": 142.0,
                    "poruka": "Penjes se na gornji sprat: pazi na led (E za akciju).",
                    "zahteva_ciscenje": False,
                },
            ],
            "prepreke": [
                pygame.Rect(130, 62, 10, 12),
                pygame.Rect(180, 106, 10, 12),
            ],
            "baklje": [(105, 68), (215, 68), (160, 48)],
            "objekti": [
                {
                    "id": "oltar_odaje",
                    "x": 152,
                    "y": 48,
                    "w": 16,
                    "h": 10,
                    "boja": (126, 88, 168),
                    "naziv": "Drevni oltar",
                    "tekst_pre": "Oltar je jos hladan; zverke moraju biti savladane.",
                    "tekst_posle": "Svetlo se budi: 'Zamak nije bio zatvor — vec utociste.'",
                }
            ],
        },
        "gornji_sprat": {
            "naziv": "Gornji sprat",
            "prolazi": [
                {
                    "rect": pygame.Rect(152, 152, 16, 10),
                    "cilj_scena": "odaja",
                    "cilj_x": 160.0,
                    "cilj_y": 48.0,
                    "poruka": "Vratio si se u odaju senki.",
                    "zahteva_ciscenje": False,
                },
            ],
            "prepreke": [
                pygame.Rect(82, 56, 10, 12),
                pygame.Rect(228, 56, 10, 12),
            ],
            "baklje": [(72, 74), (248, 74), (160, 46)],
            "objekti": [
                {
                    "id": "ogledalo_levo",
                    "x": 96,
                    "y": 42,
                    "w": 14,
                    "h": 8,
                    "boja": (110, 145, 195),
                    "naziv": "Hladno ogledalo",
                    "tekst_pre": "U staklu vidis odsjaj hodnika i natpis: 'Probudi levi fenjer...'",
                    "tekst_posle": "Ogledalo tiho odsjajuje toplinu fenjera.",
                },
                {
                    "id": "fenjer_levi",
                    "x": 64,
                    "y": 112,
                    "w": 12,
                    "h": 10,
                    "boja": (195, 115, 55),
                    "naziv": "Stari fenjer",
                    "tekst_pre": "Upalio si levi fenjer. Plamen topi mraz oko njega.",
                    "tekst_posle": "Levi fenjer vec lepo gori.",
                },
                {
                    "id": "tajni_svitak",
                    "x": 218,
                    "y": 112,
                    "w": 14,
                    "h": 10,
                    "boja": (155, 110, 190),
                    "naziv": "Skriveni svitak",
                    "tekst_pre": "Svitak je zaledjen — upali levi fenjer (E) ili savladaj cuvara.",
                    "tekst_posle": "Tajna gornjeg sprata: cuvar zamka je zaspao u ledu da sacuva ovu kucu od zla.",
                },
            ],
        },
    }


def napravi_pocetne_zverke():
    return [
        [95.0, 122.0, 20, 0.0, "spolja"],
        [185.0, 98.0, 20, 0.0, "spolja"],
        [110.0, 105.0, 20, 0.0, "hol"],
        [205.0, 105.0, 20, 0.0, "hol"],
        [140.0, 88.0, 20, 0.0, "biblioteka"],
        [135.0, 86.0, 25, 0.0, "odaja"],
        [185.0, 86.0, 25, 0.0, "odaja"],
        [160.0, 68.0, 30, 0.0, "gornji_sprat"],
    ]


def napravi_pocetno_stanje():
    return {
        "scena": "spolja",
        "igrac_x": 118.0,
        "igrac_y": 156.0,
        "vx": 0.0,
        "vy": 0.0,
        "brzina": 1.35,
        "smer_x": 0.0,
        "smer_y": -1.0,
        "hp": 100,
        "max_hp": 100,
        "nepogodiv_tajmer": 0.0,
        "napad_tajmer": 0.0,
        "napad_cooldown": 0.0,
        "poruka": "Kreni puticem ka zamku. WASD kretanje, SPACE napad, E akcija.",
        "poruka_tajmer": 5.0,
        "zverke": napravi_pocetne_zverke(),
        "prica_otkrivena": {
            "spolja": False,
            "hol": False,
            "biblioteka": False,
            "odaja": False,
            "gornji_sprat": False,
        },
        "ognjiste_iskorisceno": False,
        "oltar_aktivan": False,
        "fenjer_upaljen": False,
        "tajna_otkrivena": False,
    }


def soba_je_cista(stanje, scena):
    return all(z[2] <= 0 for z in stanje["zverke"] if z[4] == scena)


def napravi_pozadinu_spolja():
    surf = pygame.Surface((W, H))
    nebo_boje = [
        (22, 10, 46),
        (36, 14, 72),
        (56, 18, 96),
        (78, 24, 112),
        (95, 36, 118),
        (68, 32, 92),
    ]
    visina_trake = 105 // len(nebo_boje) + 1
    for i, boja in enumerate(nebo_boje):
        pygame.draw.rect(surf, boja, (0, i * visina_trake, W, visina_trake))

    planine = [(0, 92), (48, 68), (95, 86), (148, 62), (205, 84), (262, 65), (W, 88), (W, 115), (0, 115)]
    pygame.draw.polygon(surf, (28, 22, 64), planine)

    zx, zy = 162, 46
    pygame.draw.ellipse(surf, (24, 48, 34), (zx - 26, zy + 24, 52, 22))
    pygame.draw.rect(surf, (36, 30, 56), (zx - 9, zy + 8, 18, 18))
    pygame.draw.rect(surf, (44, 36, 66), (zx - 13, zy + 2, 6, 24))
    pygame.draw.rect(surf, (44, 36, 66), (zx + 7, zy + 4, 6, 22))
    pygame.draw.rect(surf, (30, 25, 48), (zx - 3, zy - 4, 6, 14))
    pygame.draw.polygon(surf, (72, 26, 58), [(zx - 14, zy + 2), (zx - 10, zy - 6), (zx - 6, zy + 2)])
    pygame.draw.polygon(surf, (72, 26, 58), [(zx + 6, zy + 4), (zx + 10, zy - 3), (zx + 14, zy + 4)])
    pygame.draw.polygon(surf, (72, 26, 58), [(zx - 4, zy - 4), (zx, zy - 12), (zx + 4, zy - 4)])
    pygame.draw.rect(surf, (20, 14, 28), (zx - 2, zy + 17, 5, 9))
    pygame.draw.rect(surf, (235, 145, 55), (zx - 1, zy + 12, 2, 2))

    pygame.draw.rect(surf, (20, 42, 28), (0, 82, W, H - 82))
    rng = random.Random(7)
    for _ in range(240):
        surf.set_at((rng.randint(0, W - 1), rng.randint(82, H - 1)), rng.choice([(26, 54, 34), (16, 34, 23), (35, 62, 36)]))

    put_tacke = [(116, 178), (128, 152), (112, 128), (138, 106), (156, 86), (163, 70)]
    pygame.draw.lines(surf, (64, 46, 34), False, put_tacke, 14)
    pygame.draw.lines(surf, (108, 78, 52), False, put_tacke, 8)
    pygame.draw.lines(surf, (136, 102, 68), False, put_tacke, 4)

    for sx in [12, 34, 58, 255, 278, 298]:
        vis_s = rng.randint(55, 92)
        top_y = max(18, 110 - vis_s)
        pygame.draw.rect(surf, (24, 15, 22), (sx - 3, top_y + 16, 6, H - (top_y + 16)))
        pygame.draw.ellipse(surf, (18, 24, 34), (sx - 14, top_y, 28, 26))

    return surf


def napravi_pozadine_soba(sobe):
    pozadine = {}
    for naziv_sobe, podaci in sobe.items():
        surf = pygame.Surface((W, H))
        if naziv_sobe == "gornji_sprat":
            surf.fill((14, 16, 30))
            pygame.draw.rect(surf, (30, 34, 58), (44, 34, W - 88, H - 60), border_radius=3)
            pygame.draw.rect(surf, (75, 92, 132), (44, 34, W - 88, H - 60), 2, border_radius=3)
            pygame.draw.rect(surf, (92, 138, 178), LED_ZONA, border_radius=3)
            pygame.draw.rect(surf, (165, 210, 238), LED_ZONA, 1, border_radius=3)
            pygame.draw.line(surf, (210, 238, 255), (LED_ZONA.x + 12, LED_ZONA.y + 10), (LED_ZONA.x + 34, LED_ZONA.y + 10), 1)
            pygame.draw.line(surf, (210, 238, 255), (LED_ZONA.x + 54, LED_ZONA.y + 28), (LED_ZONA.x + 82, LED_ZONA.y + 28), 1)
        else:
            surf.fill((16, 13, 25))
            pygame.draw.rect(surf, (34, 28, 52), (46, 36, W - 92, H - 62), border_radius=3)
            pygame.draw.rect(surf, (58, 45, 82), (46, 36, W - 92, H - 62), 2, border_radius=3)

            for gx in range(56, W - 54, 16):
                pygame.draw.line(surf, (26, 21, 40), (gx, 44), (gx, H - 34), 1)
            for gy in range(44, H - 30, 14):
                pygame.draw.line(surf, (26, 21, 40), (50, gy), (W - 50, gy), 1)

        for p in podaci["prolazi"]:
            if p["cilj_scena"] == "gornji_sprat":
                pygame.draw.rect(surf, (82, 112, 162), p["rect"])
                pygame.draw.rect(surf, (165, 205, 245), p["rect"], 1)
            else:
                pygame.draw.rect(surf, (76, 52, 36), p["rect"])
                pygame.draw.rect(surf, (132, 98, 66), p["rect"], 1)

        for prepr in podaci["prepreke"]:
            pygame.draw.rect(surf, (54, 44, 72), prepr, border_radius=2)
            pygame.draw.rect(surf, (92, 76, 118), prepr, 1, border_radius=2)

        pozadine[naziv_sobe] = surf
    return pozadine


def sudara_sa_preprekama(x, y, soba_podaci):
    igrac_box = pygame.Rect(int(x) - 3, int(y) - 3, 6, 5)
    return any(igrac_box.colliderect(p) for p in soba_podaci["prepreke"])


def pokreni_interakciju(stanje, sobe):
    igrac_rect = pygame.Rect(int(stanje["igrac_x"]) - 6, int(stanje["igrac_y"]) - 7, 12, 12)

    if stanje["scena"] == "spolja":
        vrata_spolja = pygame.Rect(156, 62, 14, 14)
        if igrac_rect.colliderect(vrata_spolja.inflate(10, 10)):
            stanje["scena"] = "hol"
            stanje["igrac_x"], stanje["igrac_y"] = 160.0, 142.0
            stanje["vx"], stanje["vy"] = 0.0, 0.0
            stanje["poruka"] = "Glavni hol zamka. Savladaj senke da otvoris desni prolaz."
            stanje["poruka_tajmer"] = 3.5
        return

    soba = sobe[stanje["scena"]]

    for p in soba["prolazi"]:
        if igrac_rect.colliderect(p["rect"].inflate(10, 10)):
            if p["zahteva_ciscenje"] and not stanje["prica_otkrivena"]["hol"]:
                stanje["poruka"] = "Prolaz je zatvoren dok ne savladas senke u holu!"
                stanje["poruka_tajmer"] = 3.0
                return

            stanje["scena"] = p["cilj_scena"]
            stanje["igrac_x"] = p["cilj_x"]
            stanje["igrac_y"] = p["cilj_y"]
            stanje["vx"], stanje["vy"] = 0.0, 0.0
            stanje["poruka"] = p["poruka"]
            stanje["poruka_tajmer"] = 3.5
            return

    for obj in soba["objekti"]:
        obj_rect = pygame.Rect(obj["x"], obj["y"], obj["w"], obj["h"]).inflate(10, 10)
        if igrac_rect.colliderect(obj_rect):
            if obj["id"] == "ognjiste_bib" and not stanje["ognjiste_iskorisceno"]:
                stanje["hp"] = min(stanje["max_hp"], stanje["hp"] + 30)
                stanje["ognjiste_iskorisceno"] = True
                stanje["poruka"] = obj["tekst_pre"]
                stanje["poruka_tajmer"] = 3.5
                return

            if obj["id"] == "fenjer_levi":
                stanje["fenjer_upaljen"] = True
                stanje["poruka"] = obj["tekst_pre"]
                stanje["poruka_tajmer"] = 3.5
                return

            if obj["id"] == "tajni_svitak":
                if stanje["fenjer_upaljen"] or soba_je_cista(stanje, "gornji_sprat"):
                    stanje["tajna_otkrivena"] = True
                    stanje["poruka"] = obj["tekst_posle"]
                    stanje["poruka_tajmer"] = 5.5
                else:
                    stanje["poruka"] = obj["tekst_pre"]
                    stanje["poruka_tajmer"] = 3.5
                return

            if obj["id"] == "oltar_odaje" and stanje["prica_otkrivena"]["odaja"]:
                stanje["oltar_aktivan"] = True
                stanje["poruka"] = obj["tekst_posle"]
                stanje["poruka_tajmer"] = 4.5
                return

            if stanje["prica_otkrivena"].get(stanje["scena"], False):
                stanje["poruka"] = obj["tekst_posle"]
            else:
                stanje["poruka"] = obj["tekst_pre"]
            stanje["poruka_tajmer"] = 4.0
            return


def azuriraj_svet(stanje, sobe, dt):
    if stanje["nepogodiv_tajmer"] > 0:
        stanje["nepogodiv_tajmer"] -= dt
    if stanje["napad_tajmer"] > 0:
        stanje["napad_tajmer"] -= dt
    if stanje["napad_cooldown"] > 0:
        stanje["napad_cooldown"] -= dt
    if stanje["poruka_tajmer"] > 0:
        stanje["poruka_tajmer"] -= dt

    if stanje["hp"] <= 0:
        return

    for s in ["spolja", "hol", "biblioteka", "odaja", "gornji_sprat"]:
        if not stanje["prica_otkrivena"][s] and soba_je_cista(stanje, s):
            stanje["prica_otkrivena"][s] = True
            if s == stanje["scena"]:
                if s == "hol":
                    stanje["poruka"] = "Senke su utihnule. Desni prolaz ka odaji sada je otvoren!"
                    stanje["poruka_tajmer"] = 4.0
                elif s == "odaja":
                    stanje["oltar_aktivan"] = True
                    stanje["poruka"] = "Odaja je mirna. Idi na vrh (E) za gornji sprat ili oltar."
                    stanje["poruka_tajmer"] = 4.5
                elif s == "biblioteka":
                    stanje["poruka"] = "Biblioteka je sada bezbedna. Proveri ognjiste ili sto."
                    stanje["poruka_tajmer"] = 3.5
                elif s == "gornji_sprat":
                    stanje["poruka"] = "Cuvar je savladan! Proveri svitak (E) za tajnu gornjeg sprata."
                    stanje["poruka_tajmer"] = 4.0

    tasteri = pygame.key.get_pressed()
    dx = (tasteri[pygame.K_RIGHT] or tasteri[pygame.K_d]) - (tasteri[pygame.K_LEFT] or tasteri[pygame.K_a])
    dy = (tasteri[pygame.K_DOWN] or tasteri[pygame.K_s]) - (tasteri[pygame.K_UP] or tasteri[pygame.K_w])

    if dx != 0 or dy != 0:
        duzina = math.hypot(dx, dy)
        dx /= duzina
        dy /= duzina
        stanje["smer_x"], stanje["smer_y"] = dx, dy

    if stanje["scena"] == "spolja":
        novi_x = max(8, min(W - 8, stanje["igrac_x"] + dx * stanje["brzina"]))
        novi_y = max(84, min(H - 6, stanje["igrac_y"] + dy * stanje["brzina"]))
        stanje["igrac_x"], stanje["igrac_y"] = novi_x, novi_y
    elif stanje["scena"] == "gornji_sprat":
        na_ledu = LED_ZONA.collidepoint(int(stanje["igrac_x"]), int(stanje["igrac_y"]))
        if na_ledu:
            stanje["vx"] = stanje["vx"] * 0.92 + dx * stanje["brzina"] * 0.16
            stanje["vy"] = stanje["vy"] * 0.92 + dy * stanje["brzina"] * 0.16
        else:
            stanje["vx"] = dx * stanje["brzina"]
            stanje["vy"] = dy * stanje["brzina"]

        levo, desno, gore, dole = SOBA_GRANICE
        novi_x = max(levo, min(desno, stanje["igrac_x"] + stanje["vx"]))
        if not sudara_sa_preprekama(novi_x, stanje["igrac_y"], sobe["gornji_sprat"]):
            stanje["igrac_x"] = novi_x
        else:
            stanje["vx"] = 0.0

        novi_y = max(gore, min(dole, stanje["igrac_y"] + stanje["vy"]))
        if not sudara_sa_preprekama(stanje["igrac_x"], novi_y, sobe["gornji_sprat"]):
            stanje["igrac_y"] = novi_y
        else:
            stanje["vy"] = 0.0
    else:
        levo, desno, gore, dole = SOBA_GRANICE
        novi_x = max(levo, min(desno, stanje["igrac_x"] + dx * stanje["brzina"]))
        if not sudara_sa_preprekama(novi_x, stanje["igrac_y"], sobe[stanje["scena"]]):
            stanje["igrac_x"] = novi_x

        novi_y = max(gore, min(dole, stanje["igrac_y"] + dy * stanje["brzina"]))
        if not sudara_sa_preprekama(stanje["igrac_x"], novi_y, sobe[stanje["scena"]]):
            stanje["igrac_y"] = novi_y

    for z in stanje["zverke"]:
        if z[4] != stanje["scena"] or z[2] <= 0:
            continue
        if z[3] > 0:
            z[3] -= dt

        dist = math.hypot(stanje["igrac_x"] - z[0], stanje["igrac_y"] - z[1])
        if 4 < dist < 85:
            brz_z = 0.55 if stanje["scena"] == "gornji_sprat" else 0.65
            zx_nov = z[0] + ((stanje["igrac_x"] - z[0]) / dist) * brz_z
            zy_nov = z[1] + ((stanje["igrac_y"] - z[1]) / dist) * brz_z
            if stanje["scena"] == "spolja" or not sudara_sa_preprekama(zx_nov, zy_nov, sobe[stanje["scena"]]):
                z[0], z[1] = zx_nov, zy_nov

        if dist < 9 and z[3] <= 0 and stanje["nepogodiv_tajmer"] <= 0:
            stanje["hp"] = max(0, stanje["hp"] - 10)
            z[3] = 1.15
            stanje["nepogodiv_tajmer"] = 0.75
            stanje["poruka"] = "Napala te je zverka! (-10 HP)"
            stanje["poruka_tajmer"] = 1.6
            if stanje["hp"] == 0:
                stanje["poruka"] = "Pao si u mraku. Pritisni R za restart."
                stanje["poruka_tajmer"] = 999.0


def iscrtaj_scenu(stanje, sobe, poz_spolja, poz_sobe, mrak, svetlo_sloj, pahulje, vreme):
    scena = stanje["scena"]
    if scena == "spolja":
        canvas.blit(poz_spolja, (0, 0))
        baklje = [(82, 138), (126, 114), (152, 92), (174, 74)]
    else:
        canvas.blit(poz_sobe[scena], (0, 0))
        baklje = list(sobe[scena]["baklje"])
        if stanje["oltar_aktivan"] and scena == "odaja":
            baklje.append((160, 56))
        if stanje["fenjer_upaljen"] and scena == "gornji_sprat":
            baklje.append((70, 112))

        for obj in sobe[scena]["objekti"]:
            boja = obj["boja"]
            if obj["id"] == "fenjer_levi" and stanje["fenjer_upaljen"]:
                boja = (245, 165, 65)
            pygame.draw.rect(canvas, boja, (obj["x"], obj["y"], obj["w"], obj["h"]), border_radius=2)
            pygame.draw.rect(canvas, (150, 125, 175), (obj["x"], obj["y"], obj["w"], obj["h"]), 1, border_radius=2)

    for idx, (bx, by) in enumerate(baklje):
        pygame.draw.rect(canvas, (72, 46, 30), (bx - 1, by, 2, 6))
        plamen_h = 4 + int(round(math.sin(vreme * 5.0 + idx * 1.9) * 1.2))
        pygame.draw.rect(canvas, (235, 110, 35), (bx - 1, by - plamen_h, 3, plamen_h))
        pygame.draw.rect(canvas, (255, 225, 110), (bx, by - max(2, plamen_h - 1), 1, max(2, plamen_h - 1)))

    for z in stanje["zverke"]:
        if z[4] == scena and z[2] > 0:
            zx_i, zy_i = int(z[0]), int(z[1])
            boja_z = (75, 130, 185) if scena == "gornji_sprat" else (32, 22, 42)
            pygame.draw.ellipse(canvas, boja_z, (zx_i - 4, zy_i - 3, 8, 5))
            pygame.draw.rect(canvas, (235, 60, 80), (zx_i + 1, zy_i - 2, 1, 1))

    ix, iy = int(stanje["igrac_x"]), int(stanje["igrac_y"])
    if stanje["nepogodiv_tajmer"] <= 0 or int(vreme * 12) % 2 == 0:
        pygame.draw.ellipse(canvas, (10, 14, 14), (ix - 4, iy + 2, 8, 3))
        pygame.draw.rect(canvas, (64, 48, 86), (ix - 3, iy - 5, 6, 8))
        pygame.draw.rect(canvas, (205, 185, 170), (ix - 2, iy - 9, 4, 4))

    if stanje["napad_tajmer"] > 0:
        hx = int(stanje["igrac_x"] + stanje["smer_x"] * 9)
        hy = int(stanje["igrac_y"] - 3 + stanje["smer_y"] * 9)
        pygame.draw.circle(canvas, (215, 225, 245), (hx, hy), 5, 1)
        pygame.draw.line(
            canvas,
            (245, 250, 255),
            (ix, iy - 3),
            (int(stanje["igrac_x"] + stanje["smer_x"] * 12), int(stanje["igrac_y"] - 3 + stanje["smer_y"] * 12)),
            2,
        )

    if scena == "gornji_sprat":
        for p in pahulje:
            p[1] += p[2]
            p[0] += math.sin(vreme + p[1] * 0.04) * 0.15
            if p[1] > H - 20:
                p[1] = 30
                p[0] = random.uniform(45, W - 45)
            canvas.set_at((int(p[0]), int(p[1])), (175, 215, 240))

    gustina_mraka = 68 if stanje["oltar_aktivan"] else (95 if scena == "gornji_sprat" else 105)
    mrak.fill((12, 8, 24, gustina_mraka))
    izvori = [(ix, iy - 4, 34, 120)]
    for idx, (bx, by) in enumerate(baklje):
        r = int(26 + math.sin(vreme * 4.2 + idx) * 3)
        izvori.append((bx, by - 2, r, 145))

    for sx, sy, radijus, alfa in izvori:
        pygame.draw.circle(mrak, (12, 8, 24, max(0, 255 - alfa)), (sx, sy), radijus)
        pygame.draw.circle(mrak, (12, 8, 24, max(0, 255 - int(alfa * 0.55))), (sx, sy), int(radijus * 0.55))

    canvas.blit(mrak, (0, 0))

    svetlo_sloj.fill((0, 0, 0, 0))
    for idx, (bx, by) in enumerate(baklje):
        r = int(14 + math.sin(vreme * 4.2 + idx) * 2)
        pygame.draw.circle(svetlo_sloj, (255, 155, 55, 36), (bx, by - 2), r)
    canvas.blit(svetlo_sloj, (0, 0))

    pygame.draw.rect(canvas, (25, 16, 32), (8, 8, 64, 7))
    hp_sirina = int(60 * (stanje["hp"] / stanje["max_hp"]))
    pygame.draw.rect(canvas, (195, 48, 68), (10, 10, hp_sirina, 3))
    pygame.draw.rect(canvas, (120, 95, 145), (8, 8, 64, 7), 1)
    canvas.blit(font.render(f"HP {stanje['hp']}", True, (235, 225, 245)), (76, 8))

    ime_sobe = "Spolja" if scena == "spolja" else sobe[scena]["naziv"]
    if stanje["tajna_otkrivena"] and scena == "gornji_sprat":
        ime_sobe = "Gornji sprat [TAJNA]"
    canvas.blit(font.render(ime_sobe, True, (195, 175, 225)), (W - 102, 8))

    if stanje["poruka_tajmer"] > 0:
        canvas.blit(font.render(stanje["poruka"], True, (240, 210, 165)), (8, H - 15))

    pygame.transform.scale(canvas, (W * SKALA, H * SKALA), prozor)
    pygame.display.flip()


def glavna():
    sobe = napravi_sobe()
    stanje = napravi_pocetno_stanje()
    poz_spolja = napravi_pozadinu_spolja()
    poz_sobe = napravi_pozadine_soba(sobe)
    mrak = pygame.Surface((W, H), pygame.SRCALPHA)
    svetlo_sloj = pygame.Surface((W, H), pygame.SRCALPHA)
    pahulje = [
        [random.uniform(45, W - 45), random.uniform(30, H - 25), random.uniform(0.15, 0.35)]
        for _ in range(22)
    ]

    vreme = 0.0
    radi = True

    while radi:
        dt = sat.tick(60) / 1000.0
        vreme += 0.08

        for dogadjaj in pygame.event.get():
            if dogadjaj.type == pygame.QUIT:
                radi = False
            elif dogadjaj.type == pygame.KEYDOWN:
                if dogadjaj.key == pygame.K_r and stanje["hp"] <= 0:
                    stanje = napravi_pocetno_stanje()
                elif dogadjaj.key == pygame.K_e and stanje["hp"] > 0:
                    pokreni_interakciju(stanje, sobe)
                elif dogadjaj.key == pygame.K_SPACE and stanje["hp"] > 0 and stanje["napad_cooldown"] <= 0:
                    stanje["napad_tajmer"] = 0.16
                    stanje["napad_cooldown"] = 0.35
                    hx = stanje["igrac_x"] + stanje["smer_x"] * 11
                    hy = stanje["igrac_y"] - 3 + stanje["smer_y"] * 11
                    for z in stanje["zverke"]:
                        if z[4] == stanje["scena"] and z[2] > 0:
                            if math.hypot(z[0] - hx, z[1] - hy) <= 13:
                                z[2] -= 15
                                if z[2] <= 0:
                                    stanje["poruka"] = "Zverka je savladana."
                                    stanje["poruka_tajmer"] = 2.0

        azuriraj_svet(stanje, sobe, dt)
        iscrtaj_scenu(stanje, sobe, poz_spolja, poz_sobe, mrak, svetlo_sloj, pahulje, vreme)

    pygame.quit()


if __name__ == "__main__":
    glavna()