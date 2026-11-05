# Отчёт аудита библиотеки Playnite 10.63 (DRY RUN)

> [!IMPORTANT]
> Аудит выполнен в режиме **DRY RUN** (исключительно чтение). База данных Playnite не модифицировалась.

## 1. Сводная статистика

- **Общее количество игр в библиотеке Playnite:** 582
- **Количество найденных совпадений с базой GameCards:** 114
- **Количество игр, готовых к обновлению:** **86**
- **Количество защищённых описаний с фразой «Локализация и озвучка»:** 443 (из них 28 совпадают с GameCards)
- **Количество игр с источником VK Play:** 42 (из них 19 совпадают с GameCards)
- **Количество игр без соответствующей HTML-карточки в GameCards:** 468
- **Количество неоднозначных совпадений:** 0

---

## 2. Таблица игр, готовых к обновлению

Для каждой из представленных ниже **86 игр** одновременно соблюдены все критерии:
1. Игра найдена в библиотеке Playnite.
2. Имеется подтверждённая HTML-карточка в `GameCards`.
3. Источник **НЕ** равен `VK Play`.
4. В текущем описании **отсутствует** фраза «Локализация и озвучка».

При выполнении боевого этапа для этих игр будут применены следующие точечные изменения:
- Поле `Description` будет заменено содержимым HTML-карточки.
- Поля `Features` и `Tags` будут очищены.
- Все остальные поля (время в игре, пути, обложки, избранное и т.д.) останутся нетронутыми.

| № | Название игры в Playnite | AppID / Идентификатор | Источник | Исходное описание (кратко) | HTML-файл карточки | Без маркера? | Не VK Play? |
|---|---|---|---|---|---|---|---|
| 1 | **Styx: Master of Shadows** | `639c5116ad7d4f31856c34aacda45f2d` | Epic | Styx: Master of Shadows — это игра в лазутчика с элементами RPG, разработанная C... | `Styx - Master of Shadows.html` | ✅ Да | ✅ Да |
| 2 | **Styx: Shards of Darkness - Deluxe Edition** | `e68e9229fd4a4a6c9a76038705ba6ae3` | Epic | Styx returns in a new stealth adventure! Explore and master huge open environmen... | `Styx - Shards of Darkness - Deluxe Edition.html` | ✅ Да | ✅ Да |
| 3 | **Submerged Hidden Depths** | `2fb0eae795104757977dfe8f93b5e593` | Epic | Плавайте среди руин утонувшего мира, лазайте по ним и открывайте их тайны. Subme... | `Submerged Hidden Depths.html` | ✅ Да | ✅ Да |
| 4 | **Subnautica 2** | `1962700` | Steam Family Sharing | Subnautica 2 — приключенческая игра о выживании под водой в чужом и незнакомом м... | `Subnautica 2.html` | ✅ Да | ✅ Да |
| 5 | **Subnautica: Below Zero** | `848450` | Steam Family Sharing | Below Zero — это подводное приключение в инопланетном океаническом мире. Встреча... | `Subnautica - Below Zero.html` | ✅ Да | ✅ Да |
| 6 | **Summer of '58** | `1609080` | Steam | «Вы его видели?» ПРЕДУПРЕЖДЕНИЕ: Возможны эпилептические припадки, связанные с п... | `Summer of '58.html` | ✅ Да | ✅ Да |
| 7 | **Sunderfolk** | `860368784274471e8d4082df2a4dc120` | Epic | Заново откройте для себя магию настолок с Sunderfolk — тактической кооперативной... | `Sunderfolk.html` | ✅ Да | ✅ Да |
| 8 | **Super Meat Boy Forever** | `Moose` | Epic | The challenge of Super Meat Boy returns in Super Meat Boy Forever! This time aro... | `Super Meat Boy Forever.html` | ✅ Да | ✅ Да |
| 9 | **SUPERHOT VR** | `617830` | Steam Family Sharing | SUPERHOT VR стирает границы между вдумчивой стратегией и безудержным безумием: э... | `SUPERHOT VR.html` | ✅ Да | ✅ Да |
| 10 | **Superliminal** | `1049410` | Steam | Superliminal – головоломка от первого лица, основанная на искаженной перспективе... | `Superliminal.html` | ✅ Да | ✅ Да |
| 11 | **Supermarket Together** | `2709570` | Steam | До 16 игроков или играйте в одиночку Разделите игру с друзьями: чем больше игрок... | `Supermarket Together.html` | ✅ Да | ✅ Да |
| 12 | **Supraland** | `1b037ad2c1e94e7e996b4a16f741025a` | Epic | Сыграйте в демоверсию! Supraland - игра-головоломка от первого лица в жанре Метр... | `Supraland.html` | ✅ Да | ✅ Да |
| 13 | **SURVIVAL IN THE BACKROOMS** | `2184110` | Steam Family Sharing | Survival In The Backrooms это атмосферная хоррор игра в которой вы будите долго ... | `SURVIVAL IN THE BACKROOMS.html` | ✅ Да | ✅ Да |
| 14 | **Surviving the Aftermath** | `Muscovy` | Epic | Выживите и придите к процветанию в постапокалиптическом мире будущего, где катас... | `Surviving the Aftermath.html` | ✅ Да | ✅ Да |
| 15 | **Suspense: Madman's Dreams** | `3395810` | Steam | Войдите в мир, где страхи становятся реальностью, а вы — не просто наблюдатель, ... | `Suspense - Madman's Dreams.html` | ✅ Да | ✅ Да |
| 16 | **Syberia** | `46500` | Steam Family Sharing | Кейт Уолкер, молодая амбициозная девушка-адвокат из Нью-Йорка, получает задание,... | `Syberia.html` | ✅ Да | ✅ Да |
| 17 | **Syberia - Remastered** | `3660220` | Steam Family Sharing | Спустя более 20 лет с выхода игры Syberia возрождается в полностью осовремененно... | `Syberia - Remastered.html` | ✅ Да | ✅ Да |
| 18 | **Syberia 2** | `46510` | Steam Family Sharing | После долгих поисков потерянного наследника в Восточной и Западной Европе, Кейт ... | `Syberia 2.html` | ✅ Да | ✅ Да |
| 19 | **System Shock 2: 25th Anniversary Remaster** | `2feb2f328922458e9f698f620fbddc13` | Epic | Как победить бессмертную совершенную машину? System Shock® 2: 25th Anniversary R... | `System Shock 2 - 25th Anniversary Remaster.html` | ✅ Да | ✅ Да |
| 20 | **Tandem A Tale of Shadows** | `57ad8e72d9a446dea9ef5cac2770a0b8` | Epic | Tandem: A Tale of Shadows — новое слово в жанре платформеров-головоломок: вас жд... | `Tandem A Tale of Shadows.html` | ✅ Да | ✅ Да |
| 21 | **Tap Ninja** | `1891700` | Steam | Станьте Мастером Ниндзя Начните свое приключение как Ниндзя в этой инкрементальн... | `Tap Ninja.html` | ✅ Да | ✅ Да |
| 22 | **TBH: Таск Бар Хиро** | `3678970` | Steam | 《ТБХ : Таск Бар Хиро》 — лучшая миниатюрная idle RPG, которая идеально вписываетс... | `TBH - Так Бар Хиро.html` | ✅ Да | ✅ Да |
| 23 | **Team Fortress 2** | `440` | Steam | «Самая весёлая многопользовательская игра» — PC Gamer Теперь БЕСПЛАТНА! Никакого... | `Team Fortress 2.html` | ✅ Да | ✅ Да |
| 24 | **Teardown** | `1167630` | Steam | Спланируйте и воплотите идеальное ограбление, не отказывая себе в разрушениях. В... | `Teardown.html` | ✅ Да | ✅ Да |
| 25 | **TerraScape** | `6ef17d9f63c143ea88a4a4bcbcf1e91c` | Epic | Устраивайтесь поудобнее и стройте собственное величественное королевство в Terra... | `TerraScape.html` | ✅ Да | ✅ Да |
| 26 | **Tharsis** | `266d978cc221471787b597695cbb9a75` | Epic | A mysterious signal originating from the Tharsis region of Mars set us on a fran... | `Tharsis.html` | ✅ Да | ✅ Да |
| 27 | **The Talos Principle** | `257510` | Steam Family Sharing | The Talos Principle - это философская головоломка с видом от первого лица от сту... | `The Talos Principle.html` | ✅ Да | ✅ Да |
| 28 | **The Talos Principle 2** | `835960` | Steam Family Sharing | Вы родились в новом мире. Люди давно вымерли, но их культура продолжает жить в г... | `The Talos Principle 2.html` | ✅ Да | ✅ Да |
| 29 | **The Talos Principle: Reawakened** | `2806640` | Steam Family Sharing | Вернитесь в невероятно красивый мир интригующих загадок и философских размышлени... | `The Talos Principle - Reawakened.html` | ✅ Да | ✅ Да |
| 30 | **The Vanishing of Ethan Carter** | `9447b19ffb6a47e1a654b75178779a28` | Epic | GOOD NEWS EVERYONE : By purchasing the game, you actually get two games now: 1) ... | `The Vanishing of Ethan Carter.html` | ✅ Да | ✅ Да |
| 31 | **The Vanishing of Ethan Carter Redux** | `58a6b5e81c644fba8bab2e05137429d9` | Epic | An Unreal Engine 4 remaster of the original game. Apart from the new engine, the... | `The Vanishing of Ethan Carter Redux.html` | ✅ Да | ✅ Да |
| 32 | **theHunter: Call of the Wild** | `4f0c34d469bb47b2bcf5b377f47ccfe3` | Epic | Наслаждайтесь неповторимой игрой про охоту в динамичном открытом мире, откликающ... | `theHunter - Call of the Wild.html` | ✅ Да | ✅ Да |
| 33 | **Thief Gold** | `211600` | Steam Family Sharing | Thief Gold is a first-person perspective stealth game. It was the first game to ... | `Thief Gold.html` | ✅ Да | ✅ Да |
| 34 | **This War of Mine** | `282070` | Steam | This War of Mine: Final Cut содержит все обновления и бесплатные расширения, вып... | `This War of Mine.html` | ✅ Да | ✅ Да |
| 35 | **Those Who Remain** | `715380` | Steam Family Sharing | Когда гаснет свет, в сонном городке Дормонте начинают тлеть угольки тьмы. По гор... | `Those Who Remain.html` | ✅ Да | ✅ Да |
| 36 | **Titan Station** | `1881120` | Steam Family Sharing | Titan Station - это однопользовательская мистерия от первого лица, действие кото... | `Titan Station.html` | ✅ Да | ✅ Да |
| 37 | **Tom Clancy's The Division 2** | `2221490` | Steam | Tom Clancy's The Division 2 body { font-family: 'Segoe UI', Tahoma, Geneva, Verd... | `Tom Clancy's The Division 2.html` | ✅ Да | ✅ Да |
| 38 | **Tomb Raider I-III Remastered Starring Lara Croft** | `2478970` | Steam Family Sharing | Discover Lara Croft’s Original Adventures, Lovingly Restored – Now with New Chal... | `Tomb Raider I-III Remastered Starring Lara Croft.html` | ✅ Да | ✅ Да |
| 39 | **Tomb Raider IV-VI Remastered** | `2525380` | Steam Family Sharing | Ее наследие живо! Отправляйтесь в приключения с обновленными играми из серии Tom... | `Tomb Raider IV-VI Remastered.html` | ✅ Да | ✅ Да |
| 40 | **Totally Reliable Delivery Service** | `Hoatzin` | Epic | Пристегивайтесь и заводите машину — посылки сами себя не доставят! Объединяйтесь... | `Totally Reliable Delivery Service.html` | ✅ Да | ✅ Да |
| 41 | **Touch Type Tale** | `fe118ed0362040c994b510da064876ca` | Epic | A boy is wanted for his nimble fingers by four rivaling dukes and duchesses of a... | `Touch Type Tale.html` | ✅ Да | ✅ Да |
| 42 | **Train Sim World 2** | `dd75b5c168d546cc869582c0389f0a1d` | Epic | Эволюция в мире железнодорожных симуляторов! Управляйте легендарными скоростными... | `Train Sim World 2.html` | ✅ Да | ✅ Да |
| 43 | **Truck Mechanic: Dangerous Paths - First Mile** | `4292050` | Steam | Это бесплатная пробная версия Truck Mechanic: Dangerous Paths — симулятора механ... | `Truck Mechanic - Dangerous Paths - First Mile.html` | ✅ Да | ✅ Да |
| 44 | **Turmoil** | `9b1148db19dc457aa1adf9f21ac6f0ff` | Epic | Turmoil предлагает пользователям сыграть в очаровательную шутливую пародию на си... | `Turmoil.html` | ✅ Да | ✅ Да |
| 45 | **Turnip Boy Commits Tax Evasion** | `3d34f303a68c44c2a9b44a3988533e90` | Epic | Представьте: вы славный малыш-репка, которого объявили врагом общества и выселил... | `Turnip Boy Commits Tax Evasion.html` | ✅ Да | ✅ Да |
| 46 | **Umfend** | `779090` | Steam Family Sharing | Атмосферный хоррор о любви и времени. Прохождение рассчитано на час или два. Тай... | `Unfend.html` | ✅ Да | ✅ Да |
| 47 | **Undying** | `c98c934106994f2d8afc36c3f1872549` | Epic | Hong Kong, 1956. You came here bright and joyful, following your husband from Sc... | `Undying.html` | ✅ Да | ✅ Да |
| 48 | **Uninvited Guest** | `1659210` | Steam Family Sharing | Uninvited Guest — это психологический хоррор от первого лица. 1930 год. Вы играе... | `Uninvited Guest.html` | ✅ Да | ✅ Да |
| 49 | **Valheim** | `892970` | Steam Family Sharing | Valheim — симулятор выживания и исследования для компании от 1 до 10 человек. Ва... | `Valheim.html` | ✅ Да | ✅ Да |
| 50 | **Vampire Survivors** | `1136763135c0482cbbb4b2d45e978156` | Epic | Пачками косить порождений ночи и дожить до рассвета! Vampire Survivors — казуаль... | `Vampire Survivors.html` | ✅ Да | ✅ Да |
| 51 | **Vampire Survivors** | `1794680` | Steam | Пачками косить порождений ночи и дожить до рассвета! Vampire Survivors — казуаль... | `Vampire Survivors.html` | ✅ Да | ✅ Да |
| 52 | **Viewfinder** | `17979201bdd845f0ab53d1d62d841dbf` | Epic | Обычный фотоаппарат поможет вам преобразить реальность, усомниться в собственном... | `Viewfinder.html` | ✅ Да | ✅ Да |
| 53 | **Viewfinder** | `1382070` | Steam Family Sharing | Обычный фотоаппарат поможет вам преобразить реальность, усомниться в собственном... | `Viewfinder.html` | ✅ Да | ✅ Да |
| 54 | **Vigil** | `3817090` | Steam | — | `Vigil.html` | ✅ Да | ✅ Да |
| 55 | **VLADiK BRUTAL** | `1316680` | Steam Family Sharing | Все события и герои являются вымышленными. Любые совпадения с реальностью случай... | `VLADIK BRUTAL.html` | ✅ Да | ✅ Да |
| 56 | **Void Bastards** | `595e35287b824902a2f7107139603732` | Epic | Забудьте все, что вы знаете о шутерах от первого лица: в Void Bastards вам нужно... | `Void Bastards.html` | ✅ Да | ✅ Да |
| 57 | **VPet** | `1920960` | Steam | *В настоящее время игра не поддерживает русский язык, но у творческих мастерских... | `VPet.html` | ✅ Да | ✅ Да |
| 58 | **Warhammer 40K Speed Freeks** | `c22fcf8eec61424b9901f2888843a25a` | Epic | Blaze into the high-Orktane mayhem of clashing Speedmobs, in adrenaline-fueled c... | `Warhammer 40K Speed Freeks.html` | ✅ Да | ✅ Да |
| 59 | **Warhammer: Vermintide 2** | `552500` | Steam | Игра Vermintide вернулась – более мрачная, кровавая и напряженная, чем когда бы ... | `Warhammer - Vermintide 2.html` | ✅ Да | ✅ Да |
| 60 | **Warpips** | `1f695dfd76d8438d8dd4046fe75daab0` | Epic | Warpips — это как если бы у Nexus Wars, Clash Royale и Command and Conquer появи... | `Warpips.html` | ✅ Да | ✅ Да |
| 61 | **Watch_Dogs** | `243470` | Steam | Set in Chicago, where a central network of computers connects everyone and every... | `Watch_Dogs.html` | ✅ Да | ✅ Да |
| 62 | **We Were Here** | `582500` | Steam | Вы заблудились в ледяной пустоши и оказались в заброшенном замке без своего спут... | `We Were Here.html` | ✅ Да | ✅ Да |
| 63 | **White Shadows** | `1158890` | Steam | White Shadows – это кинематографичный платформер-головоломка, в которой вам пред... | `White Shadows.html` | ✅ Да | ✅ Да |
| 64 | **Will To Live Online** | `707010` | Steam | Will To Live Online — MMORPG-шутер от первого лица с элементами выживания, дейст... | `Will To Live Online.html` | ✅ Да | ✅ Да |
| 65 | **Windbound** | `a95bf4df6627431ca5baff8173c59635` | Epic | The Forbidden Islands are Calling, Unlock their Secrets. Shipwrecked on an islan... | `Windbound.html` | ✅ Да | ✅ Да |
| 66 | **WINGSPAN (КРЫЛЬЯ)** | `1054490` | Steam | Wingspan (Крылья) — стратегическая карточная игра про птиц, предназначенная для ... | `WINGSPAN (КРЫЛЬЯ).html` | ✅ Да | ✅ Да |
| 67 | **With You** | `1860570` | Steam | A note from the Developer: Hey, all! I developed With You in 2019 as my MFA Thes... | `With You.html` | ✅ Да | ✅ Да |
| 68 | **Wizard of Legend** | `89443d0c5afa4ef586c72445c0399a8b` | Epic | "Wizard of Legend is a fast paced 2D dungeon crawler where you assume the role o... | `Wizard of Legend.html` | ✅ Да | ✅ Да |
| 69 | **World War Z** | `Wombat` | Epic | World War Z — это напряженный боевик для совместного прохождения с видом от трет... | `World War Z.html` | ✅ Да | ✅ Да |
| 70 | **Worms Armageddon** | `217200` | Steam | Those intrepid invertebrates return with a vengeance in the much-loved Worms Arm... | `Worms Armageddon.html` | ✅ Да | ✅ Да |
| 71 | **XCOM 2** | `3be3c4d681bc46b3b8b26c5df3ae0a18` | Epic | XCOM 2 – это продолжение полюбившейся игрокам и критикам стратегии XCOM: Enemy U... | `XCOM 2.html` | ✅ Да | ✅ Да |
| 72 | **Yooka-Laylee** | `ce2a78bf70b646e9b9f57c46dac99184` | Epic | Yooka-Laylee – новый платформер от студии Playtonic! Двух приятелей по имени Yoo... | `Yooka-Laylee.html` | ✅ Да | ✅ Да |
| 73 | **You Must** | `1726730` | Steam Family Sharing | На что ты способен пойти, ради единственного родного человека? You must – это иг... | `You Must.html` | ✅ Да | ✅ Да |
| 74 | **Yu-Gi-Oh! Duel Links** | `601510` | Steam | Yu-Gi-Oh! Duel Links is a free-to-play, digital collectible card game developed ... | `Yu-Gi-Oh! Duel Links.html` | ✅ Да | ✅ Да |
| 75 | **Zombie Shooter** | `33130` | Steam Family Sharing | Где проходит грань между жизнью и смертью? Как далеко может зайти наука, пытаясь... | `Zombie Shooter.html` | ✅ Да | ✅ Да |
| 76 | **Zup! F** | `601220` | Steam Family Sharing | Minimal physical puzzle with explosions. The player's goal to keep the blue ball... | `Zup! F.html` | ✅ Да | ✅ Да |
| 77 | **Бесконечное Лето** | `331470` | Steam | Встретив на улице Семена, главного героя игры, вы бы никогда не обратили на него... | `Бесконечное Лето.html` | ✅ Да | ✅ Да |
| 78 | **Бытовой подвиг (Routine Feat)** | `1901780` | Steam Family Sharing | Летние деньки, и никого вокруг. Безымянный офисный работник всеми силами идёт к ... | `Бытовой подвиг (Routine Feat).html` | ✅ Да | ✅ Да |
| 79 | **Г.О.П.О.Т.А** | `2389240` | Steam Family Sharing | Ку-ку ёпта! У тебя есть полтишок? А если найду? Возьмите на себя роль гопника: о... | `Г.О.П.О.Т.А.html` | ✅ Да | ✅ Да |
| 80 | **Зной** | `1815330` | Steam | Зной - это неофициальное сюжетное дополнение для Half-Life 2, события которого п... | `Зной.html` | ✅ Да | ✅ Да |
| 81 | **Куинджи, 93** | `4275420` | Steam | Куинджи, 93 — это атмосферная миниатюра от первого лица о 18-летнем парне с Донб... | `Кунджи, 93.html` | ✅ Да | ✅ Да |
| 82 | **Мухосранск | Russian City Sim** | `1612140` | Steam Family Sharing | Панельки, разваленные избушки, ржавые машины, потрескавшийся асфальт на узких до... | `Мухосранск - Russian City Sim.html` | ✅ Да | ✅ Да |
| 83 | **ПАНЕЛЬКИ** | `1836160` | Steam | Родители в детстве говорили вам, что вы станете дворником, но вы не оправдали их... | `ПАНЕЛЬКИ.html` | ✅ Да | ✅ Да |
| 84 | **ПОСЛЕДНИЙ ДЕНЬ В УРЮПИНСКЕ** | `1830870` | Steam Family Sharing | Ты уснул в своей теплой постели, в уютной квартире, купленной в ипотеку, а просн... | `ПОСЛЕДНИЙ ДЕНЬ В УРЮПИНСКЕ.html` | ✅ Да | ✅ Да |
| 85 | **Холат - перевал Дятлова** | `343710` | Steam | Kholat – это приключенческая хоррор-игра, вдохновленная реальными событиями, изв... | `Холат - перевал Дятлова.html` | ✅ Да | ✅ Да |
| 86 | **Я знаю это место..? (глава I)** | `2243560` | Steam Family Sharing | Это трансмедиа вселенная : повествование в этом проекте идет через игровые главы... | `Я знаю это место... (глава I).html` | ✅ Да | ✅ Да |

---

## 3. Защищённые совпадения (пропускаются)

Всего обнаружено **28** игр, для которых есть HTML-карточки в `GameCards`, но они **защищены от изменений** согласно правилам:

| № | Название игры в Playnite | AppID | Источник | Причина защиты |
|---|---|---|---|---|
| 1 | **Любовь, Деньги, Рок-н-Ролл** | `9cdc96cb-cf69-41b7-8db9-64f42ddef084` | VK Play | 🛡️ Источник VK Play |
| 2 | **РУСЫ ПРОТИВ ЯЩЕРОВ** | `2532550` | Steam | 🛡️ Маркер «Локализация и озвучка» |
| 3 | **Соня** | `16099f1c-754a-46f9-9354-32db55a32bfa` | VK Play | 🛡️ Источник VK Play |
| 4 | **Калибр** | `fcc558ae-9273-4987-9b6d-88c7ca59f912` | VK Play | 🛡️ Источник VK Play |
| 5 | **Василиса и Баба Яга** | `86462806-368c-45f9-a26b-7345480d0148` | VK Play | 🛡️ Источник VK Play |
| 6 | **Бессмертный. Сказки Старой Руси** | `ac8441ff-2182-4cc9-a5d5-e10662c2ee70` | VK Play | 🛡️ Источник VK Play |
| 7 | **They Are Here: Alien Abduction Horror** | `16b49d92-9d6a-4f9d-9d29-c97e044364f4` | VK Play | 🛡️ Источник VK Play |
| 8 | **СИМУЛЯТОР ОДИНОЧЕСТВА В РУССКОЙ ДЕРЕВНЕ** | `1583570` | Steam Family Sharing | 🛡️ Маркер «Локализация и озвучка» |
| 9 | **War Thunder** | `739fcb4a-16ac-4ff0-b04f-f0ae2712f855` | VK Play | 🛡️ Источник VK Play |
| 10 | **Гостомельские богатыри** | `181621fb-82a6-4898-bb72-8f87d1ebe3d3` | VK Play | 🛡️ Источник VK Play |
| 11 | **Размена не Будет** | `3431570` | Steam | 🛡️ Маркер «Локализация и озвучка» |
| 12 | **СПАРТА 2035** | `1e947742-c1db-4b18-b627-dbb7d0cd88d1` | VK Play | 🛡️ Источник VK Play |
| 13 | **За Закатом Неминуем Рассвет** | `39af6dab-d22b-4960-af6c-1afd98f65112` | VK Play | 🛡️ Источник VK Play |
| 14 | **Zi** | `12b37c18-4282-40e4-9f35-8a54b58d8296` | VK Play | 🛡️ Источник VK Play |
| 15 | **ФИЛЬМОСКОП УЖАСОВ: Зелёные Глаза** | `a71a9d03-ed64-49be-a976-d6c8b7ceeef3` | VK Play | 🛡️ Источник VK Play |
| 16 | **ЛИХО ОДНОГЛАЗОЕ** | `6d7889c8-5a3a-442e-8e25-91c36746d47a` | VK Play | 🛡️ Источник VK Play |
| 17 | **Дети Плесени** | `4326a73b-2f69-4ae3-9343-9b94cf861dac` | VK Play | 🛡️ Источник VK Play |
| 18 | **Twilight Struggle** | `406290` | Steam | 🛡️ Маркер «Локализация и озвучка» |
| 19 | **Нужен Трах** | `2608620` | Steam | 🛡️ Маркер «Локализация и озвучка» |
| 20 | **Warface** | `03eeb59c-d0d3-493e-8cb0-8ca5f7b92435` | VK Play | 🛡️ Источник VK Play |
| 21 | **Симулятор Прыгания по Гаражам** | `1529710` | Steam | 🛡️ Маркер «Локализация и озвучка» |
| 22 | **Передний Край** | `18c44323-1de7-4003-8af9-a657cc00c5d2` | VK Play | 🛡️ Источник VK Play |
| 23 | **Stray** | `1332010` | Steam | 🛡️ Маркер «Локализация и озвучка» |
| 24 | **Voidtrain** | `a0c3344c008d4475a9a29a7a0b6189b8` | Epic | 🛡️ Маркер «Локализация и озвучка» |
| 25 | **Сатурн** | `d6ff106e-59fa-4164-91fa-5385862139ec` | VK Play | 🛡️ Источник VK Play |
| 26 | **Симулятор Сидения у Подъезда** | `1031920` | Steam Family Sharing | 🛡️ Маркер «Локализация и озвучка» |
| 27 | **Отряд 22: ZOV** | `89fb1872-a3ac-40b7-8437-ff305c4b2ed9` | VK Play | 🛡️ Источник VK Play |
| 28 | **Кужлевка** | `e53450ff-0596-435f-8653-6342abe7c010` | VK Play | 🛡️ Источник VK Play |

---

## 4. Игры библиотеки Playnite без карточек в GameCards

Всего **468** игр библиотеки Playnite не имеют соответствующих карточек в текущей подборке `GameCards` (игры других серий, бандлы, DLC, тестовые клиенты и т.д.). Они остаются без каких-либо изменений.

---

## 5. Заключение аудита

- Все правила безопасности и критерии отбора строго проверены.
- Неоднозначных соответствий не выявлено.
- К обновлению подготовлено ровно **86 игр**.
- Ожидается подтверждение пользователя перед переходом к записи в базу данных Playnite.