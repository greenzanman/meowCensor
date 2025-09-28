
```
meowCensor
├─ .streamlit
│  └─ secrets.toml
├─ agents
│  ├─ audio_surgeon_agent.py
│  ├─ censor_agent.py
│  ├─ transcriber_agent.py
│  └─ __init__.py
├─ app.py
├─ context
│  ├─ design-doc.md
│  ├─ front-end
│  │  └─ front-end.md
│  ├─ implementation-plan.md
│  ├─ llms
│  │  ├─ From “Vibe Coding” to “Vibe Software Engineering”.pdf
│  │  ├─ llms-full.txt
│  │  ├─ My personal guide for developing software with AI assistance _ r_LocalLLaMA.pdf
│  │  └─ Prompting Is A Design Act_ How To Brief, Guide And Iterate With AI — Smashing Magazine.pdf
│  └─ splitting-work.md
├─ data_models.py
├─ Include
├─ Lib
├─ meow_database.csv
├─ meow_library
│  ├─ processed
│  │  ├─ 110010_cat_meow_II.wav
│  │  ├─ 110011_cat_meow.wav
│  │  ├─ 259169_CAT_MEOWwav.wav
│  │  ├─ 262312_Cat_Meow1wav.wav
│  │  ├─ 262313_Cat_Meow2wav.wav
│  │  ├─ 262314_Cat_Meow3wav.wav
│  │  ├─ 331626_Cat_Purring_and_Meowing.wav
│  │  ├─ 332980_Cat_whine_and_meow.wav
│  │  ├─ 412016_cat_purring_and_meow.wav
│  │  ├─ 412017_cat_meow_short.wav
│  │  ├─ 479271_New_Cat_Meow_2.wav
│  │  ├─ 479272_New_Cat_Meow_1.wav
│  │  ├─ 508686_SND_CatHighMeowswav.wav
│  │  ├─ 528193_Cat_Meow_2.wav
│  │  ├─ 528194_Cat_meow_3.wav
│  │  ├─ 528197_Cat_meow_1.wav
│  │  ├─ 538527_LITTLE_CAT_MEOWmp3.wav
│  │  ├─ 54057_pucky_meow_01wav.wav
│  │  ├─ 54058_pucky_meow_02wav.wav
│  │  ├─ 563280_meow_02wav.wav
│  │  ├─ 581532_my_cat_meowingwav.wav
│  │  ├─ 581534_cat_meowingwav.wav
│  │  ├─ 58981_Rabble_Meowingwav.wav
│  │  ├─ 61259_cat_meowingwav.wav
│  │  ├─ 618900_CatMeow_Smallwav.wav
│  │  ├─ 668814_Cat_meow_4.wav
│  │  ├─ 729021_Cat_Festus_Meow_1.wav
│  │  ├─ 729022_Cat_Festus_Meow_2.wav
│  │  ├─ 729023_Cat_Festus_Meow_3.wav
│  │  ├─ 729024_Cat_Festus_Meow_4.wav
│  │  ├─ 729025_Cat_Festus_Meow_5.wav
│  │  ├─ 729026_Cat_Festus_Meow_6.wav
│  │  ├─ 729027_Cat_Festus_Meow_7.wav
│  │  ├─ 729031_Cat_Smokey_Meow_1.wav
│  │  ├─ 729032_Cat_Smokey_Meow_2.wav
│  │  ├─ 730098_Cat_meowing_for_food_1.wav
│  │  ├─ 730100_Cat_meowing_for_food_3.wav
│  │  ├─ 730103_Cat_meowing_for_food_6.wav
│  │  ├─ 732519_Senior_Cat_Meow.wav
│  │  ├─ 732520_Young_Cat_Meow.wav
│  │  ├─ 732521_Begging_Meow.wav
│  │  ├─ 759416_Cat__Pearl__Meow_for_pets_2.wav
│  │  ├─ 759417_Cat__Pearl__Meow_for_pets_1.wav
│  │  ├─ 771989_Street_cat_meow.wav
│  │  ├─ 811839_meow1.wav
│  │  ├─ 811840_meow2.wav
│  │  ├─ 811841_meow3.wav
│  │  ├─ 814891_Adult_female_cat__Perran_Meow_2.wav
│  │  ├─ 814892_Adult_female_cat__Perran_Meow.wav
│  │  └─ 814893_Mature_female_cat__Pearl_Meow.wav
│  └─ raw
│     ├─ 110010_cat_meow_II.mp3
│     ├─ 110011_cat_meow.mp3
│     ├─ 259169_CAT_MEOWwav.mp3
│     ├─ 262312_Cat_Meow1wav.mp3
│     ├─ 262313_Cat_Meow2wav.mp3
│     ├─ 262314_Cat_Meow3wav.mp3
│     ├─ 331626_Cat_Purring_and_Meowing.mp3
│     ├─ 332980_Cat_whine_and_meow.mp3
│     ├─ 412016_cat_purring_and_meow.mp3
│     ├─ 412017_cat_meow_short.mp3
│     ├─ 479271_New_Cat_Meow_2.mp3
│     ├─ 479272_New_Cat_Meow_1.mp3
│     ├─ 508686_SND_CatHighMeowswav.mp3
│     ├─ 528193_Cat_Meow_2.mp3
│     ├─ 528194_Cat_meow_3.mp3
│     ├─ 528197_Cat_meow_1.mp3
│     ├─ 538527_LITTLE_CAT_MEOWmp3.mp3
│     ├─ 54057_pucky_meow_01wav.mp3
│     ├─ 54058_pucky_meow_02wav.mp3
│     ├─ 563280_meow_02wav.mp3
│     ├─ 581532_my_cat_meowingwav.mp3
│     ├─ 581534_cat_meowingwav.mp3
│     ├─ 58981_Rabble_Meowingwav.mp3
│     ├─ 61259_cat_meowingwav.mp3
│     ├─ 618900_CatMeow_Smallwav.mp3
│     ├─ 668814_Cat_meow_4.mp3
│     ├─ 729021_Cat_Festus_Meow_1.mp3
│     ├─ 729022_Cat_Festus_Meow_2.mp3
│     ├─ 729023_Cat_Festus_Meow_3.mp3
│     ├─ 729024_Cat_Festus_Meow_4.mp3
│     ├─ 729025_Cat_Festus_Meow_5.mp3
│     ├─ 729026_Cat_Festus_Meow_6.mp3
│     ├─ 729027_Cat_Festus_Meow_7.mp3
│     ├─ 729031_Cat_Smokey_Meow_1.mp3
│     ├─ 729032_Cat_Smokey_Meow_2.mp3
│     ├─ 730098_Cat_meowing_for_food_1.mp3
│     ├─ 730100_Cat_meowing_for_food_3.mp3
│     ├─ 730103_Cat_meowing_for_food_6.mp3
│     ├─ 732519_Senior_Cat_Meow.mp3
│     ├─ 732520_Young_Cat_Meow.mp3
│     ├─ 732521_Begging_Meow.mp3
│     ├─ 759416_Cat__Pearl__Meow_for_pets_2.mp3
│     ├─ 759417_Cat__Pearl__Meow_for_pets_1.mp3
│     ├─ 771989_Street_cat_meow.mp3
│     ├─ 811839_meow1.mp3
│     ├─ 811840_meow2.mp3
│     ├─ 811841_meow3.mp3
│     ├─ 814891_Adult_female_cat__Perran_Meow_2.mp3
│     ├─ 814892_Adult_female_cat__Perran_Meow.mp3
│     └─ 814893_Mature_female_cat__Pearl_Meow.mp3
├─ package-lock.json
├─ package.json
├─ peeME.md
├─ prepare-library.py
├─ pulpFictionWhat.mp3
├─ pulpFictionWhat.mp4
├─ README.md
├─ requirements.txt
├─ test.mp3
├─ tests
│  ├─ test_audio_surgeon.py
│  ├─ test_censor_agent.py
│  └─ __init__.py
├─ test_agent.py
└─ test_audio.py

```